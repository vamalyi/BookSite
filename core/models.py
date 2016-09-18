from django.db import models
from django.utils.translation import ugettext_lazy as _


class AbstractSeoContent(models.Model):
    h1 = models.CharField(_('H1'), max_length=255, null=True, blank=True)
    meta_title = models.CharField(_('Title for page'), max_length=255, null=True, blank=True)
    meta_description = models.CharField(max_length=255, null=True, blank=True)
    meta_canonical = models.CharField(max_length=255, null=True, blank=True)
    meta_keywords = models.CharField(max_length=255, null=True, blank=True)
    meta_robots = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True
