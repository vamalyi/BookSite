from django import template

from webshop import history

register = template.Library()


@register.inclusion_tag('catalogue/history/recently_viewed_products.html',
                        takes_context=True)
def recently_viewed_products(context, current_product=None):
    """
    Inclusion tag listing the most recently viewed products
    """
    request = context['request']
    products = history.get(request)
    if current_product:
        products = [p for p in products if p != current_product]
    return {'products': products,
            'request': request}
