from django import template

register = template.Library()


@register.filter(name='menu_get_lang')
def menu_get_lang(value, arg):
    print(value)
    return value
