from ckeditor.fields import RichTextField

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from core.models import AbstractSeoContent
from core.utils import image_directory_path


class Post(AbstractSeoContent):
    title = models.CharField(_('Title'), max_length=255)
    url = models.SlugField(_('URL'), max_length=255)

    TYPE = (
        ('NEWS', _('News')),
        ('ARTICLE', _('Article')),
        ('OVERVIEW', _('Overview')),
    )
    type = models.CharField(_('Type'), max_length=10, choices=TYPE, default='NEWS')

    main_image = models.ImageField(_('Main image'), upload_to=image_directory_path)
    main_image_title = models.CharField(_('Alt of main image'), max_length=255, null=True, blank=True)
    main_image_description = models.CharField(_('Title of main image'), max_length=256, null=True, blank=True)

    short_text = RichTextField(_('Short text'), blank=True, null=True)
    body = RichTextField(_('Main text'))
    additional_text = RichTextField(_('Additional text'), blank=True, null=True)

    gallery = models.ForeignKey('website.Gallery', verbose_name=_('Gallery'), blank=True, null=True)
    template = models.ForeignKey('weblayout.Template', verbose_name=_('Alternative template'), blank=True, null=True)

    created_date = models.DateTimeField(_('Created date'), auto_now_add=True)
    updated_date = models.DateTimeField(_('Updated date'), auto_now=True)

    STATUS = (
        ('DRAFT', _('Draft')),
        ('PUBLISHED', _('Published')),
    )

    status = models.CharField(_('Status'), max_length=10, choices=STATUS, default='DRAFT')

    owner = models.ForeignKey('auth.User', related_name='news', verbose_name=_('Owner of post'), null=True, blank=True)

    image_path = "news"

    class Meta:
        ordering = ['-created_date']
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def __str__(self):
        return '{} - {}'.format(self.type, self.title)

    def get_absolute_url(self):
        return reverse('news:detail', kwargs={'url': self.url, 'pk': self.pk})
