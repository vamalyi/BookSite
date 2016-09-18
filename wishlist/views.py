from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, resolve_url
from django.utils.encoding import force_text
from django.utils.http import is_safe_url
from django.views.generic import View
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView

from webaccount.views import PageTitleMixin
from webshop.models import Product
from .forms import LineFormset
from .models import WishList


def safe_referrer(request, default):
    """
    Takes the request and a default URL. Returns HTTP_REFERER if it's safe
    to use and set, and the default URL otherwise.

    The default URL can be a model with get_absolute_url defined, a urlname
    or a regular URL
    """
    referrer = request.META.get('HTTP_REFERER')
    if referrer:
        referrer = force_text(referrer)

    if referrer and is_safe_url(referrer, request.get_host()):
        return referrer
    if default:
        # Try to resolve. Can take a model instance, Django URL name or URL.
        return resolve_url(default)
    else:
        # Allow passing in '' and None as default
        return default


class WishListAddProduct(View):
    """
    Adds a product to a wish list.

    - If the user doesn't already have a wishlist then it will be created for
      them.
    - If the product is already in the wish list, its quantity is increased.
    """

    def dispatch(self, request, *args, **kwargs):
        self.product = get_object_or_404(Product, pk=kwargs['product_pk'])
        self.wishlist = self.get_or_create_wishlist(request, *args, **kwargs)
        return super(WishListAddProduct, self).dispatch(request)

    def get_or_create_wishlist(self, request, *args, **kwargs):
        wishlists = request.user.wishlists.all()[:1]
        if not wishlists:
            return request.user.wishlists.create()
        wishlist = wishlists[0]

        if not wishlist.is_allowed_to_edit(request.user):
            raise PermissionDenied
        return wishlist
    #
    # def get(self, request, *args, **kwargs):
    #     # This is nasty as we shouldn't be performing write operations on a GET
    #     # request.  It's only included as the UI of the product detail page
    #     # allows a wishlist to be selected from a dropdown.
    #     return self.add_product()

    def post(self, request, *args, **kwargs):
        return self.add_product()

    def add_product(self):
        self.wishlist.add(self.product)
        msg = _("'%s' було додано у список бажань.") % self.product.name
        messages.success(self.request, msg)
        return redirect(safe_referrer(self.request, self.product.get_absolute_url()))
        # return redirect('account:wishlist:wishlists-detail')


class WishListDetailView(PageTitleMixin, FormView):
    """
    This view acts as a DetailView for a wish list and allows updating the
    quantities of products.

    It is implemented as FormView because it's easier to adapt a FormView to
    display a product then adapt a DetailView to handle form validation.
    """
    template_name = 'account/wishlist/wishlists_detail.html'
    active_tab = "wishlist"
    form_class = LineFormset

    def dispatch(self, request, *args, **kwargs):
        key = kwargs.get('key', None)
        if key:
            self.object = self.get_wishlist_or_404(key, request.user)
        else:
            self.object = self.get_or_create_wishlist(request, *args, **kwargs)

        return super(WishListDetailView, self).dispatch(request, *args, **kwargs)

    def get_or_create_wishlist(self, request, *args, **kwargs):
        wishlists = request.user.wishlists.all()[:1]
        if not wishlists:
            return request.user.wishlists.create()
        wishlist = wishlists[0]

        if not wishlist.is_allowed_to_edit(request.user):
            raise PermissionDenied
        return wishlist

    def get_wishlist_or_404(self, key, user):
        wishlist = get_object_or_404(WishList, key=key)
        if wishlist.is_allowed_to_see(user):
            return wishlist
        else:
            raise Http404

    def get_page_title(self):
        return self.object.name

    def get_form_kwargs(self):
        kwargs = super(WishListDetailView, self).get_form_kwargs()
        kwargs['instance'] = self.object
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super(WishListDetailView, self).get_context_data(**kwargs)
        ctx['wishlist'] = self.object
        other_wishlists = self.request.user.wishlists.exclude(
            pk=self.object.pk)
        ctx['other_wishlists'] = other_wishlists
        return ctx

    def form_valid(self, form):
        for subform in form:
            if subform.cleaned_data.get('quantity', 1) <= 0 or subform.cleaned_data.get('DELETE', False):
                subform.instance.delete()
            else:
                subform.save()
        return redirect('account:wishlist:wishlists-detail')
