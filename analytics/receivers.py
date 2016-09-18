import logging

from django.db import IntegrityError
from django.db.models import F
from django.dispatch import receiver

from analytics.models import UserSearch, UserProductView, UserRecord, ProductRecord
from search.signals import user_search
from webshop.signals import product_viewed

logger = logging.getLogger('shop.analytics')


def _update_counter(model, field_name, filter_kwargs, increment=1):
    """
    Efficiently updates a counter field by a given increment. Uses Django's
    update() call to fetch and update in one query.

    :param model: The model class of the recording model
    :param field_name: The name of the field to update
    :param filter_kwargs: Parameters to the ORM's filter() function to get the
                          correct instance
    """
    try:
        record = model.objects.filter(**filter_kwargs)
        affected = record.update(**{field_name: F(field_name) + increment})
        if not affected:
            filter_kwargs[field_name] = increment
            model.objects.create(**filter_kwargs)
    except IntegrityError:
        # get_or_create sometimes fails due to MySQL's weird transactions, fail
        # silently
        logger.error(
            "IntegrityError when updating analytics counter for %s", model)

# Receivers


@receiver(product_viewed)
def receive_product_view(sender, product, user, **kwargs):
    if kwargs.get('raw', False):
        return
    _update_counter(ProductRecord, 'num_views', {'product': product})
    if user and user.is_authenticated():
        _update_counter(UserRecord, 'num_product_views', {'user': user})
        UserProductView.objects.create(product=product, user=user)


@receiver(user_search)
def receive_product_search(sender, query, user, **kwargs):
    if user and user.is_authenticated() and not kwargs.get('raw', False):
        UserSearch._default_manager.create(user=user, query=query)
