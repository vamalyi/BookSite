import re

from django.core.validators import RegexValidator, _lazy_re_compile
from django.utils.translation import ugettext_lazy as _


slug_re = _lazy_re_compile(r'^[-\/a-zA-Z0-9_]+\Z')
validate_slug_with_slash = RegexValidator(
    slug_re,
    _("Enter a valid 'slug' consisting of letters, numbers, underscores, slash or hyphens."),
    'invalid'
)
slug_unicode_re = _lazy_re_compile(r'^[-\/\w]+\Z', re.U)
validate_unicode_slug_with_slash = RegexValidator(
    slug_unicode_re,
    _("Enter a valid 'slug' consisting of Unicode letters, numbers, underscores, or hyphens."),
    'invalid'
)
