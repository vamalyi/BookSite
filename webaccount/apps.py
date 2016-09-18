from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AccountConfig(AppConfig):
    label = 'webaccount'
    name = 'webaccount'
    verbose_name = _('Account')

    def ready(self):
        from . import receivers  # noqa
