from django import template

from weblayout.models import Menu

register = template.Library()


@register.assignment_tag
def get_menu(name):
    menu = Menu.objects.filter(name=name)
    return menu.get().items.all() if menu.exists() else []
