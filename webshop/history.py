import json

from django.conf import settings

from analytics.models import UserProductView
from webshop.models import Product


def get(request):
    """
    Return a list of recently viewed products
    """
    ids = extract(request)

    product_dict = Product.objects.in_bulk(ids)
    ids.reverse()
    return [product_dict[id] for id in ids if id in product_dict]


def extract(request, response=None):
    """
    Extract the IDs of products in the history cookie
    """
    ids = []
    cookie_name = settings.RECENTLY_VIEWED_COOKIE_NAME
    if cookie_name in request.COOKIES:
        try:
            ids = json.loads(request.COOKIES[cookie_name])
        except ValueError:
            # This can occur if something messes up the cookie
            if response:
                response.delete_cookie(cookie_name)
        else:
            # Badly written web crawlers send garbage in double quotes
            if not isinstance(ids, list):
                ids = []

    max_products = settings.RECENTLY_VIEWED_PRODUCTS
    if len(ids) < max_products:
        user_ids = []
        if request.user.is_authenticated():
            ids_user_db = list(UserProductView.objects.filter(user=request.user).exclude(product_id__in=ids).order_by(
                '-date_created').values_list('product_id', flat=True))
            for i in ids_user_db:
                if not i in user_ids:
                    user_ids.append(i)
            user_ids.reverse()

        ids = user_ids + ids
    return ids


def add(ids, new_id):
    """
    Add a new product ID to the list of product IDs
    """
    max_products = settings.RECENTLY_VIEWED_PRODUCTS
    if new_id in ids:
        ids.remove(new_id)
    ids.append(new_id)
    if len(ids) > max_products:
        ids = ids[len(ids) - max_products:]
    return ids


def update(product, request, response):
    """
    Updates the cookies that store the recently viewed products
    removing possible duplicates.
    """
    ids = extract(request, response)
    updated_ids = add(ids, product.id)
    response.set_cookie(
        settings.RECENTLY_VIEWED_COOKIE_NAME,
        json.dumps(updated_ids),
        max_age=settings.RECENTLY_VIEWED_COOKIE_LIFETIME,
        secure=settings.RECENTLY_VIEWED_COOKIE_SECURE,
        httponly=True)


def login_update(request, response):
    ids = extract(request, response)

    user_ids = []
    if request.user.is_authenticated():
        ids_user_db = list(UserProductView.objects.filter(user=request.user).exclude(pk__in=ids).order_by(
            '-date_created').values_list('product_id', flat=True))
        for i in ids_user_db:
            if not i in user_ids:
                user_ids.append(i)
        user_ids.reverse()

    ids = user_ids + ids
    max_products = settings.RECENTLY_VIEWED_PRODUCTS
    if len(ids) > max_products:
        ids = ids[len(ids) - max_products:]

    response.set_cookie(
        settings.RECENTLY_VIEWED_COOKIE_NAME,
        json.dumps(ids),
        max_age=settings.RECENTLY_VIEWED_COOKIE_LIFETIME,
        secure=settings.RECENTLY_VIEWED_COOKIE_SECURE,
        httponly=True)
