from django.core.exceptions import ObjectDoesNotExist
from django import template

from website.models import Variable

register = template.Library()


@register.assignment_tag
def get_variables_by_namespace(namespace):
    return Variable.objects.filter(namespace=namespace).order_by('name')


@register.simple_tag
def get_variable_by_name(name):
    try:
        return Variable.objects.get(name=name).value
    except ObjectDoesNotExist:
        return 'Variable with name {} does not exist'.format(name)
