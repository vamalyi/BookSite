from django import http
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.core.urlresolvers import reverse
from django.db import transaction, IntegrityError
from django.db.models import F
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.utils.translation import ugettext_lazy as _

from webaccount.models import UserProfile, UserAddress, UserPhoneNumber
from webform.forms import send_email
from webshop.models import Product, ProductPriceCorrector
from webshopcart.forms import OrderForm, OrderLoginForm, OrderRegistrationForm
from website.models import GlobalSettings

from .utils import create_cart_order, create_order_item

User = get_user_model()


class BasketView(TemplateView):
    template_name = 'basket/basket.html'
    login_prefix, registration_prefix, order_prefix = 'login', 'registration', 'order'
    order_form_class = OrderForm
    login_form_class = OrderLoginForm
    registration_form_class = OrderRegistrationForm
    redirect_field_name = 'next'
    tabs = ('order', 'login_order', 'registration_order')

    def get_products(self):
        products = []
        cart_products = self.request.session.get('cart', {})
        if cart_products == {}:
            return {}

        product_ids = cart_products.keys()
        _products = list(Product.objects.filter(pk__in=product_ids))

        for product in _products:
            for _corrector in cart_products[str(product.id)]:
                count = int(cart_products[str(product.id)][_corrector])
                if _corrector == 'None':
                    price = float(product.get_default_price)
                    corrector = None
                else:
                    corrector = ProductPriceCorrector.objects.get(pk=_corrector)
                    price = float(corrector.get_new_price_with_coefficient)
                products.append((product, corrector, count, price, price * count))

        return products

    def post(self, request, *args, **kwargs):
        self.total = sum(map(lambda a: a[4], self.get_products()))
        if u'order_submit' in request.POST:
            return self.validate_order_form()
        if u'login_submit' in request.POST:
            return self.validate_login_form()
        elif u'registration_submit' in request.POST:
            return self.validate_registration_form()
        return http.HttpResponseBadRequest()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        if 'form' not in kwargs:
            ctx['form'] = self.order_form_class(**self.get_order_form_kwargs())
        if not (self.request.user and self.request.user.is_authenticated()):
            if 'login_form' not in kwargs:
                ctx['login_form'] = self.login_form_class(**self.get_login_form_kwargs())
            if 'registration_form' not in kwargs:
                ctx['registration_form'] = self.registration_form_class(**self.get_registration_form_kwargs())

        products = self.get_products()

        ctx['products'] = products
        ctx['total_price'] = float(sum(map(lambda a: a[4], products)))

        if 'tab' not in kwargs:
            tab = self.request.GET.get('tab', 'default')
            tab = tab if tab in self.tabs else 'default'
            ctx['tab'] = tab

        return ctx

    def get_order_form_kwargs(self, bind_data=False):
        kwargs = {
            'initial': {},
            'prefix': self.order_prefix
        }

        if bind_data and self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        kwargs['owner'] = self.request.user

        return kwargs

    def get_login_form_kwargs(self, bind_data=False):
        kwargs = {}
        kwargs['host'] = self.request.get_host()
        kwargs['prefix'] = self.login_prefix
        kwargs['initial'] = {
            'redirect_url': self.request.GET.get(self.redirect_field_name, ''),
        }
        if bind_data and self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_registration_form_kwargs(self, bind_data=False):
        kwargs = self.get_login_form_kwargs(bind_data=bind_data)
        kwargs['prefix'] = self.registration_prefix

        return kwargs

    def validate_order_form(self):
        form = self.order_form_class(**self.get_order_form_kwargs(bind_data=True))
        if form.is_valid():
            user = self.request.user

            if user and user.is_authenticated():
                name = user.username
                email = user.email
            else:
                user = None
                name = form.cleaned_data['username']
                email = form.cleaned_data['email']
            return self.complete_order(form, name, email, user)

        ctx = self.get_context_data(form=form, tab='order')
        return self.render_to_response(ctx)

    def validate_login_form(self):
        form = self.login_form_class(**self.get_login_form_kwargs(bind_data=True))
        if form.is_valid():
            login(self.request, form.get_user())
            user = self.request.user

            if user and user.is_authenticated():
                name = user.username
                email = user.email
            else:
                return http.HttpResponseBadRequest()
            return self.complete_order(form, name, email, user)

        ctx = self.get_context_data(login_form=form, tab='login_order')
        return self.render_to_response(ctx)

    def validate_registration_form(self):
        form = self.registration_form_class(**self.get_registration_form_kwargs(bind_data=True))
        if form.is_valid():
            user = self.register_user(form)

            if user and user.is_authenticated():
                name = user.username
                email = user.email
            else:
                return http.HttpResponseBadRequest()
            return self.complete_order(form, name, email, user)

        ctx = self.get_context_data(registration_form=form, tab='registration_order')
        return self.render_to_response(ctx)

    def complete_order(self, form, name, email, user):
        description = form.cleaned_data['description']
        phone = form.cleaned_data['phone']
        delivery = form.cleaned_data['delivery']
        shipping_address = ''

        city = form.cleaned_data['delivery_city']
        warehouses = form.cleaned_data['delivery_warehouses']

        if delivery.code == 'nova_poshta':
            if city and warehouses:
                if description:
                    description = '{}\n\nГород: {}\nОтделение: {}'.format(description, city, warehouses)
                else:
                    description = 'Город: {}\nОтделение: {}'.format(city, warehouses)
            else:
                return http.HttpResponseBadRequest()
        elif delivery.code == 'city':
            shipping_address = form.cleaned_data['shipping_address']

        if user:
            user_profile, c = UserProfile.objects.get_or_create(user=user)
            if shipping_address:
                address, created = UserAddress.objects.get_or_create(user=user_profile, defaults={
                    'line1': shipping_address,
                    'is_default_for_shipping': True,
                    'num_orders': 1
                })
                if not created and address.line1 == shipping_address:
                    address.num_orders = F('num_orders') + 1
                    address.save()
            if phone and not user_profile.phone_numbers.exists():
                UserPhoneNumber.objects.create(user=user_profile, phone_number=phone,
                                               is_default_phone_number=True)

        total = self.total + float(delivery.price)
        products_in_cart = self.request.session['cart']

        try:
            with transaction.atomic():
                cart_order = create_cart_order(total, name, email, description, phone, user, delivery,
                                               shipping_address)
                create_order_item(products_in_cart, cart_order)
        except IntegrityError:
            messages.error(self.request, 'При сохранении заказа возникла ошибка. Заказ не сохранен.')
            return HttpResponseRedirect(reverse('basket'))

        ctx = {
            'subject': _('New order'),
            'message': '',
            'total_price': total,
            'products': products_in_cart,
            'basket': cart_order,
            'phone': phone,
            'address': shipping_address,
            'description': description,
        }

        recipient_list = [email]
        send_email(recipient_list, ctx, 'email/order_user.html')

        global_settings = GlobalSettings.objects
        if global_settings.exists():
            recipient_list = global_settings.first().emails.replace('\r', '').replace('\n', '').split(',')
            recipient_list = [mail.replace(' ', '') for mail in recipient_list]
            send_email(recipient_list, ctx, 'email/order_admin.html')

        if self.request.session.get('cart') is not None:
            del self.request.session['cart']

        return HttpResponseRedirect('/thanks_order/')

    def register_user(self, form):
        user = form.save()
        try:
            user = authenticate(
                username=user.username,
                password=form.cleaned_data['password1'])
        except User.MultipleObjectsReturned:
            users = User.objects.filter(email=user.email)
            user = users[0]
            for u in users[1:]:
                u.is_active = False
                u.save()

        login(self.request, user)

        return user
