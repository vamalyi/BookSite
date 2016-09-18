from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from webaccount.forms import EmailAuthenticationForm, EmailUserCreationForm
from webshop.models import DeliveryRule
from webshopcart.models import ProductCart


class OrderMixin(forms.Form):
    description = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': _('Note'),
        'rows': 6,
    }), required=False)
    delivery = forms.ModelChoiceField(queryset=DeliveryRule.objects.all(), empty_label=None, to_field_name='code',
                                      widget=forms.Select(attrs={
                                          'class': 'form-control',
                                          'style': 'color:#000;font-size:12px;width:97%;'
                                      }))
    delivery_city = forms.CharField(widget=forms.HiddenInput(), required=False)
    delivery_warehouses = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['delivery'] = 'without_delivery'

    def clean(self):
        if self.cleaned_data['delivery'].code == 'nova_poshta' and not (self.cleaned_data['delivery_city'] and
                                                                       self.cleaned_data['delivery_warehouses']):
            self.add_error(None, ValidationError('Оберіть місто та відділення Нової Пошти.'))
        return self.cleaned_data


class OrderForm(forms.ModelForm, OrderMixin):
    redirect_url = forms.CharField(
        widget=forms.HiddenInput, required=False)

    class Meta:
        model = ProductCart
        fields = ('username', 'phone', 'email', 'description', 'delivery', 'shipping_address')
        widgets = {
            'username': forms.TextInput(attrs={
                'required': 'required',
                'placeholder': _("Ваше ім'я"),
            }),
            'phone': forms.TextInput(attrs={
                'required': 'required',
                'type': 'tel',
                'placeholder': _('Phone'),
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': _('Email'),
            }),
            'shipping_address': forms.Textarea(attrs={
                'placeholder': _('Shipping address'),
                'class': 'hidden',
            })
        }

    def __init__(self, owner=None, sum=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone'].required = True
        self.initial['fixed_sum'] = sum
        if owner and owner.is_authenticated():
            self.instance.owner = owner
            self.adjust_field(owner)

    def adjust_field(self, owner):
        # self.instance.email = owner.email
        self.initial['email'] = owner.email
        address = owner.userprofile.addresses.first()
        phone = owner.userprofile.phone_numbers.first()
        if address:
            self.initial['shipping_address'] = address.line1
        if phone:
            self.initial['phone'] = phone.phone_number
        # self.instance.username = owner.username
        self.initial['username'] = owner.get_full_name()
        # self.fields['username'].widget = forms.HiddenInput()
        self.fields['email'].widget = forms.HiddenInput()

    def clean(self):
        if self.cleaned_data['delivery'].code == 'nova_poshta' and not (self.cleaned_data['delivery_city'] and
                                                                       self.cleaned_data['delivery_warehouses']):
            self.add_error(None, ValidationError('Оберіть місто та відділення Нової Пошти.'))
        return self.cleaned_data


class OrderLoginForm(OrderMixin, EmailAuthenticationForm):
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'required': 'required',
        'type': 'tel',
        'placeholder': _('Phone'),
    }))
    shipping_address = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': _('Shipping address'),
        'class': 'hidden',
    }), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class OrderRegistrationForm(OrderMixin, EmailUserCreationForm):
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'required': 'required',
        'type': 'tel',
        'placeholder': _('Phone'),
    }))
    shipping_address = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': _('Shipping address'),
        'class': 'hidden',
    }), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
