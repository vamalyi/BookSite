from django import forms
from django.core.mail import send_mail
from webshop.models import ProductReview, Product
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _

from webrating.models import Rating
from frankie_web_platform.settings import SEND_FROM_EMAIL, RECIPIENT_LIST_ADMIN, \
    RECIPIENT_LIST_FEEDBACK
from website.models import GlobalSettings


class FormFeedback(forms.Form):
    user_name = forms.CharField(label=_('Name'), max_length=100, error_messages={'required': _('Error. Name')})
    user_email = forms.CharField(label='E-mail', max_length=100, required=False)
    user_phone = forms.CharField(label=_('Phone'), max_length=13,
                                 error_messages={'required': _('Error. Phone')})
    user_message = forms.CharField(label=_('Message'), max_length=255, widget=forms.Textarea, required=False)

    @staticmethod
    def process(request):
        form_feedback = FormFeedback(request.POST or None)
        if request.POST and form_feedback.is_valid():
            subject = "admin@gmail.com"
            user_name = form_feedback.cleaned_data['user_name']
            user_email = form_feedback.cleaned_data['user_email']
            user_phone = form_feedback.cleaned_data['user_phone']
            user_message = form_feedback.cleaned_data['user_message']
            message = user_name + '\n' + user_phone + '\n' + user_message + '\n' + user_email
            recipients = RECIPIENT_LIST_FEEDBACK
            send_mail(subject, message, 'TEST !!!', recipients)
            print(request)
            return True, form_feedback
        else:
            return False, form_feedback


class FormRatingGlobal(forms.Form):
    user_name = forms.CharField(label=_('Name'), max_length=100, error_messages={'required': _('Error. Name')})
    user_email = forms.CharField(label='E-mail', max_length=100, required=False)
    user_rating = forms.FloatField(label=_('Rating'), error_messages={'required': _('Error. Phone')})
    user_message = forms.CharField(label=_('Message'), max_length=255, widget=forms.Textarea, required=True,
                                   error_messages={'required': _('Error. Message')})

    @staticmethod
    def process(request):
        if request.POST:
            form_rating = FormRatingGlobal(request.POST or None)
            if request.POST and form_rating.is_valid():
                user_name = form_rating.cleaned_data['user_name']
                user_email = form_rating.cleaned_data['user_email']
                user_rating = form_rating.cleaned_data['user_rating']
                user_message = form_rating.cleaned_data['user_message']
                rating = Rating()
                rating.user_name = user_name
                rating.rating = user_rating
                rating.comment = user_message
                rating.email = user_email
                rating.save()

                # subject = "test"
                # message = user_name + '\n' + user_rating.__str__() + '\n' + user_message + '\n' + user_email
                # recipients = ['deniszorinets@gmail.com']
                # send_mail(subject, message, 'TEST !!!', recipients)
                return True, form_rating
            else:
                return False, form_rating


class FormRating(forms.Form):
    user_name = forms.CharField(label=_('Name'), max_length=100, error_messages={'required': _('Error. Name')})
    product_id = forms.FloatField(widget=forms.HiddenInput())
    user_email = forms.CharField(label='E-mail', max_length=100, required=False)
    user_rating = forms.FloatField(label=_('Rating'), error_messages={'required': _('Error. Phone')})
    user_message = forms.CharField(label=_('Message'), max_length=255, widget=forms.Textarea, required=True,
                                   error_messages={'required': _('Error. Message')})

    @staticmethod
    def process(request):
        if request.POST:
            form_rating = FormRating(request.POST or None)
            if request.POST and form_rating.is_valid():
                user_name = form_rating.cleaned_data['user_name']
                user_email = form_rating.cleaned_data['user_email']
                user_rating = form_rating.cleaned_data['user_rating']
                user_message = form_rating.cleaned_data['user_message']
                rating = ProductReview()
                rating.user_name = user_name
                rating.rating = user_rating
                rating.product = Product.objects.filter(id=form_rating.cleaned_data['product_id']).first()
                rating.comment = user_message
                rating.email = user_email
                rating.save()

                # subject = "test"
                # message = user_name + '\n' + user_rating.__str__() + '\n' + user_message + '\n' + user_email
                # recipients = ['deniszorinets@gmail.com']
                # send_mail(subject, message, 'TEST !!!', recipients)
                return True, form_rating
            else:
                return False, form_rating


def send_email(recipient_list, ctx, template_name):
    global_settings = GlobalSettings.objects.first()
    html_template = get_template(template_name)

    company = global_settings.company_name
    subject = ctx.get('subject', company)
    message = ctx.get('message', '')
    from_email = SEND_FROM_EMAIL.format(company=company)
    fail_silently = False
    auth_user = None
    auth_password = None
    connection = None
    html_message = html_template.render(ctx)
    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently,
        auth_user,
        auth_password,
        connection,
        html_message
    )


def OrderSendAdmin(request, data=None):
    if request.POST:
        post = request.POST
        html_template = get_template('webform/order_send_admin.html')

        total_sum = 0
        if data:
            for p in data:
                total_sum += p.sum

        subject = _('New order.')
        message = ''
        from_email = SEND_FROM_EMAIL
        recipient_list = RECIPIENT_LIST_ADMIN
        fail_silently = False
        auth_user = None
        auth_password = None
        connection = None
        html_message = html_template.render({
            'user_name': post['user_name'],
            'user_phone': post['user_phone'],
            'user_email': post['user_email'],
            'products': data,
            'total_sum': total_sum
        })
        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently,
            auth_user,
            auth_password,
            connection,
            html_message
        )
    return True


def OrderSendUser(request, data=None):
    if request.POST:
        post = request.POST
        html_template = get_template('webform/order_send_user.html')

        total_sum = 0
        if data:
            for p in data:
                total_sum += p.sum

        user_email = ''
        if post['user_email']:
            user_email = post['user_email']
        else:
            user_email = 'alexander.mediaset@gmail.com'

        subject = 'MONA COLLECTION - Новый заказ'
        message = ''
        from_email = SEND_FROM_EMAIL
        recipient_list = user_email,
        fail_silently = False
        auth_user = None
        auth_password = None
        connection = None
        html_message = html_template.render({
            'user_name': post['user_name'],
            'user_phone': post['user_phone'],
            'user_email': post['user_email'],
            'products': data,
            'total_sum': total_sum
        })
        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently,
            auth_user,
            auth_password,
            connection,
            html_message
        )
    return True
