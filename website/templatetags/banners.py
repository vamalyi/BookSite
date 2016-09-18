from django import template
from django.core.exceptions import ObjectDoesNotExist

from website.models import Banner, Gallery

register = template.Library()


@register.inclusion_tag('partials/slider.html')
def render_banner(banner_name):
    try:
        return {'banners': Banner.objects.get(name=banner_name).banners.all()}
    except ObjectDoesNotExist:
        return {'banners': []}


@register.inclusion_tag('partials/slider.html')
def render_gallery(gallery_name):
    return {'banners': Gallery.objects.get(name=gallery_name).images.all()}
