from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ShopConfig(AppConfig):
    label = 'webshop'
    name = 'webshop'
    verbose_name = _('Shop')

    def ready(self):
        from . import receivers  # noqa
