from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.db import models

from core.fields import SlugWithSlashField
from core.utils import image_directory_path


class Template(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, unique=True)
    path = models.CharField(max_length=256, unique=True)
    creation_date = models.DateField(auto_now_add=True, blank=True)
    last_edit_date = models.DateField(auto_now=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'templates'
        verbose_name = _('Template')
        verbose_name_plural = _('Templates')


class SystemElement(models.Model):
    ELEMENT_TYPE = (
        ('Header', _('Header')),
        ('Footer', _('Footer')),
        ('Script', _('Script'))
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=16, choices=ELEMENT_TYPE, unique=True)
    body = RichTextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'system_elements'
        verbose_name = _('System Element')
        verbose_name_plural = _('System Elements')


class Menu(models.Model):
    name = models.CharField(max_length=120)

    class Meta:
        verbose_name = _('Menu')
        verbose_name_plural = _('Menu')

    def __str__(self):
        return self.name


class MenuItem(MPTTModel):
    alternative_name = models.CharField(_('Alternative name'), max_length=120, null=True, blank=True)
    alternative_url = SlugWithSlashField(_('Alternative url'), max_length=255, null=True, blank=True)
    image = models.ImageField(_('Image of menu item'), upload_to=image_directory_path, null=True, blank=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children',
                            verbose_name='Parent menu item')
    content_type = models.ForeignKey(ContentType, null=True, blank=True, limit_choices_to={
        'model__in': ('product', 'category', 'staticpage', 'prefilter')
    })
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey()
    menu = models.ForeignKey(Menu, related_name='items', verbose_name='Menu')
    image_path = "menu_items"

    class Meta:
        verbose_name = _('Menu item')
        verbose_name_plural = _('Menu items')

    def __str__(self):
        if hasattr(self.content_object, 'name'):
            return '{} of {}'.format(self.content_object.name, self.menu)
        if self.alternative_name:
            return '{} of {}'.format(self.alternative_name, self.menu)
        return 'None of {}'.format(self.menu)

    def save(self, *args, **kwargs):
        if self.alternative_url and self.alternative_url[0] != '/':
            self.alternative_url = '/{}'.format(self.alternative_url)
        if self.alternative_url and self.alternative_url[-1] != '/':
            self.alternative_url = '{}/'.format(self.alternative_url)
        super().save(*args, **kwargs)
