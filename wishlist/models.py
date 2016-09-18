import hashlib
import random

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import six
from django.utils.translation import ugettext_lazy as _, pgettext_lazy
from webshop.models import Product


class WishList(models.Model):
    """
    Represents a user's wish lists of products.

    A user can have multiple wish lists, move products between them, etc.
    """

    # Only authenticated users can have wishlists
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name='wishlists', verbose_name=_('Owner'))
    name = models.CharField(verbose_name=_('Name'), default=_('Default'),
                            max_length=255)

    #: This key acts as primary key and is used instead of an int to make it
    #: harder to guess
    key = models.CharField(_('Key'), max_length=6, db_index=True, unique=True,
                           editable=False)

    date_created = models.DateTimeField(
        _('Date created'), auto_now_add=True, editable=False)

    class Meta:
        app_label = 'wishlist'
        ordering = ('owner', 'date_created',)
        verbose_name = _('Wish List')

    def __str__(self):
        return u"%s's Wish List '%s'" % (self.owner, self.name)

    def save(self, *args, **kwargs):
        if not self.pk or kwargs.get('force_insert', False):
            self.key = self.__class__.random_key()
        super(WishList, self).save(*args, **kwargs)

    @classmethod
    def random_key(cls, length=6):
        """
        Get a unique random generated key based on SHA-1 and owner
        """
        while True:
            rand = six.text_type(random.random()).encode('utf8')
            key = hashlib.sha1(rand).hexdigest()[:length]
            if not cls._default_manager.filter(key=key).exists():
                return key

    def is_allowed_to_see(self, user):
        return user == self.owner

    def is_allowed_to_edit(self, user):
        return user == self.owner

    def get_absolute_url(self):
        return reverse('account:wishlist:wishlists-detail', kwargs={
            'key': self.key})

    def add(self, product):
        """
        Add a product to this wishlist
        """
        lines = self.lines.filter(product=product)
        if len(lines) == 0:
            self.lines.create(
                product=product, title=product.name)
        else:
            line = lines[0]
            line.quantity += 1
            line.save()


class Line(models.Model):
    """
    One entry in a wish list. Similar to order lines or basket lines.
    """
    wishlist = models.ForeignKey('wishlist.WishList', on_delete=models.CASCADE,
                                 related_name='lines',
                                 verbose_name=_('Wish List'))
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, verbose_name=_('Product'),
        related_name='wishlists_lines',
        blank=True, null=True)
    quantity = models.PositiveIntegerField(_('Quantity'), default=1)
    #: Store the title in case product gets deleted
    title = models.CharField(
        pgettext_lazy(u"Product title", u"Title"), max_length=255)

    class Meta:
        app_label = 'wishlist'
        # Enforce sorting by order of creation.
        ordering = ['pk']
        unique_together = (('wishlist', 'product'),)
        verbose_name = _('Wish list line')

    def __str__(self):
        return u'%sx %s on %s' % (self.quantity, self.title,
                                  self.wishlist.name)

    def get_title(self):
        if self.product:
            return self.product.name
        else:
            return self.title
