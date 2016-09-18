from django import forms
from django.utils.translation import ugettext_lazy as _


class SearchForm(forms.Form):
    q = forms.CharField(max_length=256,
                        widget=forms.TextInput(attrs={
                                    # 'class': 'form-control',
                                    'placeholder': _('Search'),
                                    'required': 'required'}))
