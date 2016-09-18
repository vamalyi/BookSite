import json
import requests

from django.conf import settings
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.http import JsonResponse

from webshop.models import Product, ProductPriceCorrector


def get_nova_poshta_cities(request):
    data = json.dumps({
        "modelName": "Address",
        "calledMethod": "getCities",
        "apiKey": settings.NOVA_POSHTA_KEY,
        "methodProperties": {},
    })
    data = requests.get('https://api.novaposhta.ua/v2.0/json/', data=data).json()
    data = [{'city': d['DescriptionRu'], 'code': d['Ref']} for d in data['data']]
    data = {'data': data, 'status': 'OK'}
    return JsonResponse(data, charset='utf-8')


def get_nova_poshta_warehouses(request, city):
    # city = "db5c88ce-391c-11dd-90d9-001a92567626"
    data = json.dumps({
        "modelName": "Address",
        "calledMethod": "getWarehouses",
        "apiKey": settings.NOVA_POSHTA_KEY,
        "methodProperties": {
            "CityRef": city
        },
    })
    data = requests.get('https://api.novaposhta.ua/v2.0/json/', data=data).json()
    data = [{'city': d['DescriptionRu'], 'code': d['Ref']} for d in data['data']]
    data = {'data': data, 'status': 'OK'}
    return JsonResponse(data, charset='utf-8')


def get_products(cart_products):
    products = []
    if cart_products == {}:
        return {}

    product_ids = cart_products.keys()
    _products = list(Product.objects.filter(pk__in=product_ids))

    for product in _products:
        for _corrector in cart_products[str(product.id)]:
            count = int(cart_products[str(product.id)][_corrector])
            if _corrector == 'None':
                price = float(product.get_default_price)
                corrector = None
            else:
                corrector = ProductPriceCorrector.objects.get(pk=_corrector)
                price = float(corrector.get_new_price_with_coefficient)
            products.append((product, corrector, count, price, price * count))

    return products


def add_product(request, overwrite_count=False):
    if request.POST:
        product_id = request.POST.get('id')
        price_corrector_id = request.POST.get('price_corrector_id', 'None')
        price_corrector_id = 'None' if price_corrector_id == '' else price_corrector_id
        count = request.POST.get('count') or 1
        if int(count) < 1:
            count = 1

        product = Product.objects.filter(pk=product_id)
        if not product.exists():
            return JsonResponse({'result': False, 'error': _('Product not found'), 'data': ''}, charset='utf-8')
        if price_corrector_id not in ('', 'None'):
            if not ProductPriceCorrector.objects.filter(pk=price_corrector_id, product=product).exists():
                return JsonResponse({'result': False, 'error': _('ProductPriceCorrector not found'), 'data': ''},
                                    charset='utf-8')

        if 'cart' in request.session:
            if product_id in request.session['cart'].keys():
                if price_corrector_id in request.session['cart'][product_id].keys():
                    if overwrite_count:
                        request.session['cart'][product_id][price_corrector_id] = count
                    else:
                        new_count = int(request.session['cart'][product_id][price_corrector_id]) + int(count)
                        request.session['cart'][product_id][price_corrector_id] = new_count
                else:
                    request.session['cart'][product_id][price_corrector_id] = count
            else:
                request.session['cart'][product_id] = {price_corrector_id: count}
        else:
            request.session['cart'] = {product_id: {price_corrector_id: count}}

        products = get_products(request.session['cart'])
        ctx = {'products': products, 'total_price': sum(map(lambda a: a[4], products))}
        basket_html = render_to_string('basket/partials/basket_content.html', RequestContext(request, ctx))

        count = 0
        for product_id in request.session.get('cart', []):
            for price_corrector in request.session['cart'][product_id].keys():
                count += int(request.session['cart'][product_id][price_corrector])

        data = {
            'content_html': basket_html,
            'count': count,
            'sum': ctx['total_price'],
        }

        return JsonResponse({'result': True, 'error': None, 'data': data}, charset='utf-8')


def set_product(request):
    return add_product(request, True)


def del_product(request):
    if request.POST:
        product_id = request.POST.get('id')
        price_corrector_id = request.POST.get('price_corrector_id', 'None')
        price_corrector_id = 'None' if price_corrector_id == '' else price_corrector_id

        if 'cart' in request.session:
            if product_id in request.session['cart'].keys():
                if (len(request.session['cart'][product_id]) == 1 and
                            tuple(request.session['cart'][product_id].keys())[0] == price_corrector_id):
                    del request.session['cart'][product_id]
                elif (len(request.session['cart'][product_id]) > 1 and
                              price_corrector_id in request.session['cart'][product_id].keys()):
                    del request.session['cart'][product_id][price_corrector_id]
                else:
                    return JsonResponse({'result': False, 'error': _('ProductPriceCorrector not in cart'), 'data': ''},
                                        charset='utf-8')
            else:
                return JsonResponse({'result': False, 'error': _('Product not in cart'), 'data': ''},
                                    charset='utf-8')
        else:
            return JsonResponse({'result': False, 'error': _('Cart not found'), 'data': ''},
                                charset='utf-8')

        products = get_products(request.session['cart'])
        ctx = {'products': products, 'total_price': sum(map(lambda a: a[4], products))}
        basket_html = render_to_string('basket/partials/basket_content.html', RequestContext(request, ctx))

        count = 0
        for product_id in request.session.get('cart', []):
            for price_corrector in request.session['cart'][product_id].keys():
                count += int(request.session['cart'][product_id][price_corrector])

        data = {
            'content_html': basket_html,
            'count': count,
            'sum': ctx['total_price'],
        }

        return JsonResponse({'result': True, 'error': None, 'data': data}, charset='utf-8')
