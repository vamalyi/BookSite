import json

from django.http import HttpResponseRedirect
from django.utils.encoding import uri_to_iri

import webshopcart.models as wshcm
import webform.forms as wff
import webshop.models as wshm


class Product:
    def __init__(self, product_id, url, name, price, image, corrector_id=None):
        self.product_id = product_id
        self.corrector_id = corrector_id
        self.url = url
        self.name = name
        self.price = price
        self.image = image


class ProductOrder:
    def __init__(self, name, count, price):
        self.name = name
        self.count = count
        self.price = price
        self.sum = (float(count) * price)


def create_cart_order(total, user_name, email, description, phone, user=None, delivery=None, shipping_address=''):
    cart_order = wshcm.ProductCart()
    cart_order.username = user_name
    cart_order.email = email
    cart_order.fixed_sum = total
    cart_order.description = description
    cart_order.phone = phone
    cart_order.shipping_address = shipping_address
    if user and user.is_authenticated():
        cart_order.owner = user
    if delivery:
        cart_order.delivery = delivery
    cart_order.save()

    return cart_order


def get_product_in_cart(cart_object):
    products_in_cart = []
    for product in cart_object['products']:
        if product['data']['price_correctors'].__len__() > 0:
            for corrector in product['data']['price_correctors']:
                products_in_cart.append({
                    'product_id': product['id'],
                    'count': corrector['data']['count'],
                    'price_corrector_id': corrector['id'],
                })
        else:
            products_in_cart.append({
                'product_id': product['id'],
                'count': product['data']['count'],
                'price_corrector_id': None,
            })
    return products_in_cart


def create_order_item(products_in_cart, cart_order):
    for product_id in products_in_cart.keys():
        for corrector_id in products_in_cart[product_id]:
            product_tmp = wshcm.ProductInCart()
            product_tmp.product_id = product_id
            product_tmp.cart = cart_order
            product_tmp.count = products_in_cart[product_id][corrector_id]
            if corrector_id and corrector_id != 'None':
                product_tmp.price_correction = wshm.ProductPriceCorrector.objects.filter(
                    id=corrector_id).first()
            product_tmp.save()


def send_email(request, products_in_cart):
    products_order = []
    for p in products_in_cart:
        tmp = wshm.Product.objects.filter(id=p['product_id']).first()
        if p['price_corrector_id']:
            price = wshm.ProductPriceCorrector.objects.filter(
                id=p['price_corrector_id']).first()
            products_order.append(ProductOrder(tmp.name, p['count'], price.get_new_price))
        else:
            products_order.append(ProductOrder(tmp.name, p['count'], tmp.get_default_price))

    wff.OrderSendAdmin(request, products_order)
    wff.OrderSendUser(request, products_order)


def create_cart(request):
    if request.COOKIES.get('productsInCart', None):
        cart_order = create_cart_order(float(request.POST['totalPrice']), request.POST['user_name'],
                                       request.POST['user_email'], request.POST['description'],
                                       request.POST['user_phone'])

        cart_object = json.loads(uri_to_iri(request.COOKIES['productsInCart']))
        products_in_cart = get_product_in_cart(cart_object)

        create_order_item(products_in_cart, cart_order)

        # Send mail reports:
        send_email(request, products_in_cart)

        return HttpResponseRedirect('/thanks_order/')
