from django import forms
from django.utils.translation import ugettext_lazy as _

from webshop.models import ProductTreeReview


class ProductReviewForm(forms.ModelForm):
    name = forms.CharField(label=_('Name'), required=True)
    email = forms.EmailField(label=_('Email'), required=True)

    def __init__(self, product, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.product = product
        if user and user.is_authenticated():
            self.instance.user = user
            del self.fields['name']
            del self.fields['email']
            if user.is_staff:
                self.instance.status = ProductTreeReview.APPROVED

    class Meta:
        model = ProductTreeReview
        fields = ('score', 'body', 'name', 'email', 'parent')
        widgets = {
            'parent': forms.HiddenInput(),
        }


class ProductShortReviewForm(forms.ModelForm):
    name = forms.CharField(label=_('Name'), required=True)
    email = forms.EmailField(label=_('Email'), required=True)

    def __init__(self, product, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.product = product
        if user and user.is_authenticated():
            self.instance.user = user
            del self.fields['name']
            del self.fields['email']
            if user.is_staff:
                self.instance.status = ProductTreeReview.APPROVED

    class Meta:
        model = ProductTreeReview
        fields = ('body', 'name', 'email', 'parent')
        widgets = {
            'parent': forms.HiddenInput(),
        }
