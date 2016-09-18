from django import template

from webshop.models import Product, ProductPriceCorrector

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_products(context):
    products = []
    cart_products = context['request'].session.get('cart', {})
    if cart_products == {}:
        return {}

    product_ids = cart_products.keys()
    _products = list(Product.objects.filter(pk__in=product_ids))

    for product in _products:
        for _corrector in cart_products[str(product.id)]:
            count = int(cart_products[str(product.id)][_corrector])
            if _corrector == 'None':
                price = int(product.get_default_price)
                corrector = None
            else:
                corrector = ProductPriceCorrector.objects.get(pk=_corrector)
                price = int(corrector.get_new_price_with_coefficient)
            products.append((product, corrector, count, price, price * count))
    total_price = sum(map(lambda a: a[4], products))

    return products, total_price
