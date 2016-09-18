import re

from django.conf import settings

import weblayout.models as wlm
from webshop.models import Product, Manufacturer


def sys_elements(request):
    sys_elem = wlm.SystemElement.objects.all()
    sys_header = sys_elem.filter(name='Header').first()
    sys_footer = sys_elem.filter(name='Footer').first()
    sys_script = sys_elem.filter(name='Script').first()

    sys_elem = {
        'sys_header': sys_header,
        'sys_footer': sys_footer,
        'sys_script': sys_script,
    }

    return sys_elem


def manufacturers(request):
    manufacturer_list = Manufacturer.objects.exclude(slug='empty')
    menu = {
        # 'manufacturer_list': manufacturer_list.filter(
        #     products__in=Product.objects.only('manufacturer').distinct('manufacturer'))
        'manufacturer_list': manufacturer_list
    }
    return menu


def basket_count(request):
    count = 0
    product_ids = []
    for product_id in request.session.get('cart', []):
        for price_corrector in request.session['cart'][product_id].keys():
            count += int(request.session['cart'][product_id][price_corrector])
        product_ids.append(product_id)

    return {'basket_count': count, 'cart_products': set([int(i) for i in product_ids])}


def strip_language_code(request):
    """
    When using Django's i18n_patterns, we need a language-neutral variant of
    the current URL to be able to use set_language to change languages.
    This naive approach strips the language code from the beginning of the URL
    and will likely fail if using translated URLs.
    """
    path = request.path
    if settings.USE_I18N and hasattr(request, 'LANGUAGE_CODE'):
        return re.sub('^/%s/' % request.LANGUAGE_CODE, '/', path)
    return path


def metadata(request):
    """
    Add some generally useful metadata to the template context
    """
    return {'display_version': getattr(settings, 'DISPLAY_VERSION', False),
            'version': getattr(settings, 'VERSION', 'N/A'),
            'shop_name': settings.SHOP_NAME,
            'homepage_url': settings.HOMEPAGE,
            'language_neutral_url_path': strip_language_code(request),
            }
