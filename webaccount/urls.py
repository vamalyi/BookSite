from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from wishlist.views import WishListAddProduct, WishListDetailView

from webaccount.views import AccountAuthView, AccountEditView, logout_view, UserOrdersView, UserDetailOrderView, \
    AccountSettingsView, ProfileEditView, CallbackProfileView

wishlist_urlpatterns = (
    [
        url(r'^$', login_required(WishListDetailView.as_view()), name='wishlists-detail'),
        url(r'^(?P<key>[a-z0-9]+)/$', login_required(WishListDetailView.as_view()), name='wishlists-detail'),
        url(r'^add/(?P<product_pk>\d+)/$', login_required(WishListAddProduct.as_view()), name='wishlists-add-product'),
    ], 'wishlist')

urlpatterns = [
    url(r'^login/$', AccountAuthView.as_view(), name='login_registration'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^profile/$', login_required(AccountEditView.as_view()), name='profile'),
    url(r'^profile/settings/$', login_required(AccountSettingsView.as_view()), name='settings'),
    url(r'^profile/edit/$', login_required(ProfileEditView.as_view()), name='edit'),
    url(r'^profile/callback/$', login_required(CallbackProfileView.as_view()), name='callback'),
    url(r'^profile/orders/$', login_required(UserOrdersView.as_view()), name='profile_orders'),
    url(r'^profile/order/(?P<pk>\d+)/$', login_required(UserDetailOrderView.as_view()), name='profile_order'),
    url(r'^wishlists/', include(wishlist_urlpatterns, namespace='wishlist')),
]
