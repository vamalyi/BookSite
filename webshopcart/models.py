from decimal import Decimal
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

# WebShop Models
from webshop.models import Product, ProductPriceCorrector, DeliveryRule

# Chained selects support
from smart_selects.db_fields import ChainedForeignKey


def get_default_delivery():
    delivery = DeliveryRule.objects
    return delivery.get(code='without_delivery').id if delivery.filter(code='without_delivery') else 1


class ProductInCart(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, verbose_name=_('Product'))
    cart = models.ForeignKey('ProductCart', related_name='order_items', verbose_name=_('Cart'))
    count = models.PositiveIntegerField(_('Quantity of products'))
    price_correction = ChainedForeignKey(
        ProductPriceCorrector,
        chained_field="product",
        chained_model_field="product",
        show_all=False,
        auto_choose=True,
        null=True,
        blank=True,
        verbose_name=_('Price corrector')
    )

    def price(self):
        sale = 0
        if self.product.sale:
            sale -= self.product.sale.percent / 100
        margin = 0
        if self.product.margin:
            margin += self.product.margin.percent / 100
        sale_margin = Decimal(1 + sale + margin)
        if self.price_correction:
            price = self.price_correction.get_new_price_with_coefficient * self.count * sale_margin
            return price.quantize(Decimal('0.01'))
        price = self.product.get_default_price * self.count * sale_margin
        return price.quantize(Decimal('0.01'))

    def __str__(self):
        return str.format("{0} ({1}) = {2}",
                          self.product, self.count, self.price())

    class Meta:
        db_table = 'products_in_carts'
        verbose_name = _('Product in Cart')
        verbose_name_plural = _('Products in Carts')


class ProductCart(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='baskets', null=True,
                              verbose_name=_("Owner"))
    username = models.CharField(_('Name'), max_length=256)
    email = models.EmailField(_('Email'), max_length=256, null=True, blank=True)
    phone = models.CharField(_('Phone'), max_length=256)
    description = models.TextField(_('Note'), max_length=256, null=True, blank=True)
    date_on_add = models.DateTimeField(_('Date created'), auto_now_add=True)
    date_on_close = models.DateTimeField(_('Date updated'), null=True, blank=True)
    closed = models.BooleanField(_('Is complete?'), default=False)
    paid = models.BooleanField(_('Is paid?'), default=False)
    fixed_sum = models.DecimalField(_('Order price'), decimal_places=2, max_digits=12, null=True, blank=True)

    delivery = models.ForeignKey(DeliveryRule, related_name='baskets', default=get_default_delivery,
                                 verbose_name=_('Delivery rule'))
    shipping_address = models.TextField(_('Shipping address'), blank=True)

    def __str__(self):
        return str.format("User: {0} || Email: {1} || Phone: {2} || Description: {3} || Date: {4}",
                          self.username, self.email, self.phone, self.description, self.date_on_add)

    @property
    def number(self):
        return '{:0>5}'.format(self.id)

    def all_products(self):
        products = ProductInCart.objects.filter(cart=self).all()
        res = ''
        for product in products:
            res += product.__str__() + '</br>'
        return res

    def sum(self):
        products = ProductInCart.objects.filter(cart=self).all()
        res = 0
        for product in products:
            res += product.price()
        return res

    all_products.allow_tags = True

    def check_sum(self):
        if self.fixed_sum == self.sum():
            return True
        return False

    class Meta:
        db_table = 'product_carts'
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')
