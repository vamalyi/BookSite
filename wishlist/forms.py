from django import forms
from django.forms.models import inlineformset_factory

from .models import WishList, Line


class WishListLineForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(WishListLineForm, self).__init__(*args, **kwargs)
        # self.fields['quantity'].widget.attrs['class'] = 'input-mini'


# LineFormset = inlineformset_factory(
#     WishList, Line, fields=('quantity', 'id'), form=WishListLineForm,
#     extra=0, can_delete=True)
LineFormset = inlineformset_factory(
    WishList, Line, fields=('id',), form=WishListLineForm,
    extra=0, can_delete=True)
