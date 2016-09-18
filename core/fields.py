from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _

from core.validators import validate_slug_with_slash, validate_unicode_slug_with_slash


class FormSlugField(forms.CharField):
    default_validators = [validate_slug_with_slash]

    def __init__(self, *args, **kwargs):
        self.allow_unicode = kwargs.pop('allow_unicode', False)
        if self.allow_unicode:
            self.default_validators = [validate_unicode_slug_with_slash]
        super().__init__(*args, **kwargs)


class SlugWithSlashField(models.CharField):
    default_validators = [validate_slug_with_slash]
    description = _("Slug (up to %(max_length)s)")

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 50)
        # Set db_index=True unless it's been set manually.
        if 'db_index' not in kwargs:
            kwargs['db_index'] = True
        self.allow_unicode = kwargs.pop('allow_unicode', False)
        if self.allow_unicode:
            self.default_validators = [validate_unicode_slug_with_slash]
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if kwargs.get("max_length") == 50:
            del kwargs['max_length']
        if self.db_index is False:
            kwargs['db_index'] = False
        else:
            del kwargs['db_index']
        if self.allow_unicode is not False:
            kwargs['allow_unicode'] = self.allow_unicode
        return name, path, args, kwargs

    def get_internal_type(self):
        return "SlugField"

    def formfield(self, **kwargs):
        defaults = {'form_class': FormSlugField, 'allow_unicode': self.allow_unicode}
        defaults.update(kwargs)
        return super().formfield(**defaults)
