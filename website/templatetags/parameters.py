from django import template
from django.core.exceptions import ObjectDoesNotExist

from webshop.models import ProductParameterAvailableValue, ProductParameter

register = template.Library()


@register.simple_tag
def get_parameter_value(product, parameter_id):
    try:
        parameter = product.parameter_values.get(product_parameter=parameter_id)
        return parameter.value.value
    except ObjectDoesNotExist:
        return ''


@register.assignment_tag
def get_car_classes():
    return ProductParameterAvailableValue.objects.filter(
        product_parameter=ProductParameter.objects.get(pk=9)).order_by('weight')
