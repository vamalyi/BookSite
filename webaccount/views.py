from django.forms.formsets import all_valid
from extra_views import UpdateWithInlinesView, InlineFormSet
from django import http
from django.conf import settings
from django.contrib.auth import login, authenticate, get_user_model, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import TemplateView, UpdateView, ListView, DetailView
from django.utils.translation import ugettext_lazy as _

from webaccount.models import UserAddress, UserPhoneNumber, UserProfile
from webform.forms import send_email
from webshop import history
from webshopcart.models import ProductCart
from website.models import GlobalSettings
from .forms import EmailAuthenticationForm, EmailUserCreationForm, EmailUserChangeForm, UserChangeForm, UserAddressForm, \
    UserPhoneNumberForm, ProfileForm, CallbackForm

User = get_user_model()


class PageTitleMixin(object):
    page_title = None
    active_tab = None

    # Use a method that can be overridden and customised
    def get_page_title(self):
        return self.page_title

    def get_context_data(self, **kwargs):
        ctx = super(PageTitleMixin, self).get_context_data(**kwargs)
        ctx.setdefault('page_title', self.get_page_title())
        ctx.setdefault('active_tab', self.active_tab)
        return ctx


def logout_view(request):
    cart = request.session.get('cart')
    logout(request)
    if cart is not None:
        request.session['cart'] = cart

    response = http.HttpResponseRedirect(settings.HOMEPAGE)
    for cookie in settings.COOKIES_DELETE_ON_LOGOUT:
        response.delete_cookie(cookie)
    return response


class AccountSettingsView(PageTitleMixin, UpdateView):
    model = User
    form_class = UserChangeForm
    active_tab = 'settings'
    template_name = 'account/settings.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect(settings.LOGIN_URL)
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('account:settings')


class AccountEditView(PageTitleMixin, TemplateView):
    active_tab = 'profile'
    template_name = 'account/profile.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect(settings.LOGIN_URL)
        return super().get(request, *args, **kwargs)


class AccountAuthView(TemplateView):
    template_name = 'account/login_registration.html'
    login_prefix, registration_prefix = 'login', 'registration'
    login_form_class = EmailAuthenticationForm
    registration_form_class = EmailUserCreationForm
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super(AccountAuthView, self).get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        ctx = super(AccountAuthView, self).get_context_data(**kwargs)
        if 'login_form' not in kwargs:
            ctx['login_form'] = self.get_login_form()
        if 'registration_form' not in kwargs:
            ctx['registration_form'] = self.get_registration_form()
        return ctx

    def post(self, request, *args, **kwargs):
        if u'login_submit' in request.POST:
            return self.validate_login_form()
        elif u'registration_submit' in request.POST:
            return self.validate_registration_form()
        return http.HttpResponseBadRequest()

    def get_login_form(self, bind_data=False):
        return self.login_form_class(
            **self.get_login_form_kwargs(bind_data))

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

    def validate_login_form(self):
        form = self.get_login_form(bind_data=True)
        if form.is_valid():

            login(self.request, form.get_user())

            response = redirect(self.get_login_success_url(form))
            history.login_update(self.request, response)

            return response

        ctx = self.get_context_data(login_form=form)
        return self.render_to_response(ctx)

    @staticmethod
    def get_login_success_url(form):
        redirect_url = form.cleaned_data['redirect_url']
        if redirect_url:
            return redirect_url

        return settings.LOGIN_REDIRECT_URL

    def get_registration_form(self, bind_data=False):
        return self.registration_form_class(
            **self.get_registration_form_kwargs(bind_data))

    def get_registration_form_kwargs(self, bind_data=False):
        kwargs = self.get_login_form_kwargs(bind_data=bind_data)
        kwargs['prefix'] = self.registration_prefix

        return kwargs

    def validate_registration_form(self):
        form = self.get_registration_form(bind_data=True)
        if form.is_valid():
            self.register_user(form)

            return redirect(self.get_registration_success_url(form))

        ctx = self.get_context_data(registration_form=form)
        return self.render_to_response(ctx)

    @staticmethod
    def get_registration_success_url(form):
        redirect_url = form.cleaned_data['redirect_url']
        if redirect_url:
            return redirect_url

        return settings.LOGIN_REDIRECT_URL

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


class UserOrdersView(PageTitleMixin, ListView):
    model = ProductCart
    page_title = _('Orders')
    active_tab = 'orders'
    template_name = 'account/order_list.html'
    context_object_name = 'orders'
    paginate_by = settings.PROFILE_ORDERS_ON_PAGE

    def get_queryset(self):
        orders = super().get_queryset().filter(owner=self.request.user).order_by('-date_on_add')

        return orders


class UserDetailOrderView(PageTitleMixin, DetailView):
    model = ProductCart
    page_title = _('Order')
    active_tab = 'orders'
    template_name = 'account/order_detail.html'
    context_object_name = 'order'

    def get(self, request, *args, **kwargs):
        order = self.get_object()
        if order.owner and order.owner == request.user:
            return super().get(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('account:profile_orders'))

    def get_queryset(self):
        orders = super().get_queryset().prefetch_related('order_items')

        return orders


class UserAddressInline(InlineFormSet):
    model = UserAddress
    form_class = UserAddressForm
    extra = 1
    max_num = 1
    can_delete = False


class UserPhoneNumberInline(InlineFormSet):
    model = UserPhoneNumber
    form_class = UserPhoneNumberForm
    extra = 1
    max_num = 1
    can_delete = False


class ProfileEditView(PageTitleMixin, UpdateWithInlinesView):
    active_tab = 'profile_edit'
    model = UserProfile
    form_class = ProfileForm
    inlines = [UserAddressInline, UserPhoneNumberInline]
    template_name = 'account/profile_edit.html'

    def get_object(self, queryset=None):
        user, _ = UserProfile.objects.get_or_create(user=self.request.user)
        return user

    def get_success_url(self):
        return reverse('account:edit')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user and self.request.user.is_authenticated():
            kwargs.update({'user': self.request.user})
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            self.object = form.save(commit=False)
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            User.objects.filter(pk=request.user.id).update(first_name=first_name, last_name=last_name)
            form_validated = True
        else:
            form_validated = False

        inlines = self.construct_inlines()

        if all_valid(inlines) and form_validated:
            return self.forms_valid(form, inlines)
        return self.forms_invalid(form, inlines)


class CallbackProfileView(TemplateView):
    template_name = 'account/callback.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect(settings.LOGIN_URL)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        if 'form' not in ctx:
            ctx['form'] = CallbackForm(user=self.request.user)

        return ctx

    def post(self, request, *args, **kwargs):
        form = CallbackForm(user=self.request.user, data=self.request.POST, files=self.request.FILES)

        global_settings = GlobalSettings.objects
        if form.is_valid() and global_settings.exists():
            recipient_list = [form.cleaned_data['email']]
            ctx = {
                'subject': 'Callback',
                'title': form.cleaned_data['title'],
                'message': form.cleaned_data['body'],
            }

            send_email(recipient_list, ctx, 'email/account_callback_user.html')

            recipient_list = global_settings.first().emails.replace('\r', '').replace('\n', '').split(',')
            recipient_list = [mail.replace(' ', '') for mail in recipient_list]

            send_email(recipient_list, ctx, 'email/account_callback.html')

            return HttpResponseRedirect(reverse('thanks_callback'))

        return self.render_to_response(self.get_context_data(form=form))
