from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Ckeditor support
from ckeditor.fields import RichTextField

# Image croppig support and thumbnails engine
from image_cropping import ImageRatioField
from easy_thumbnails.files import get_thumbnailer
from core.utils import image_directory_path

# WebLayout models
from core.models import AbstractSeoContent
from weblayout.models import Template

# Config variables
from frankie_web_platform.settings import GALLERY_IMAGE_LARGE, GALLERY_IMAGE_MEDIUM, GALLERY_IMAGE_SMALL


class StaticPage(AbstractSeoContent):
    id = models.AutoField(primary_key=True)
    name = models.CharField(_('Name'), max_length=256, unique=True)
    url = models.CharField(_('URL'), max_length=256, unique=True)
    first_text = RichTextField(_('First text'), null=True, blank=True)
    second_text = RichTextField(_('Second text'), null=True, blank=True)
    gallery = models.ForeignKey('Gallery', verbose_name=_('Gallery'), null=True, blank=True)
    template = models.ForeignKey(Template, verbose_name=_('Alternative template'), blank=True, null=True)
    creation_date = models.DateField(_('Date created'), auto_now_add=True, blank=True)
    last_edit_date = models.DateField(_('Date updated'), auto_now=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        if self.url == 'index':
            return reverse('home_page')
        return reverse('page', args=(self.url,))

    class Meta:
        db_table = 'static_pages'
        verbose_name = _('Static Page')
        verbose_name_plural = _('Static Pages')


class GalleryImagePosition(models.Model):
    id = models.AutoField(primary_key=True)
    image_original = models.ImageField(_('Original image'),
                                       upload_to=image_directory_path)
    cropping_large = ImageRatioField('image_original', GALLERY_IMAGE_LARGE)
    cropping_medium = ImageRatioField('image_original', GALLERY_IMAGE_MEDIUM)
    cropping_small = ImageRatioField('image_original', GALLERY_IMAGE_SMALL)

    name = models.CharField(_('Name'), max_length=256, unique=True)
    title = models.CharField(_('Title'), max_length=256)
    creation_date = models.DateField(_('Date created'), auto_now_add=True, blank=True)
    last_edit_date = models.DateField(_('Date updated'), auto_now=True, blank=True)
    weight = models.IntegerField(_('Weight'))
    active = models.BooleanField(_('Is active?'), default=True)
    description = models.CharField(_('Description'), max_length=256, null=True, blank=True)
    gallery = models.ForeignKey('Gallery', related_name='images', verbose_name=_('Gallery'))

    image_path = 'image_positions/galleries'

    def __str__(self):
        return self.name

    def original_image(self):
        return str.format("/media/{0}", self.image_original, self.title)

    original_image.short_description = _('Original image')
    original_image.allow_tags = True

    def original_image_admin(self):
        return str.format("<img src=/media/{0} alt='Original Image: {1}' width=100/>", self.image_original, self.title)

    def large_image(self):
        url = get_thumbnailer(self.image_original).get_thumbnail({
            'size': (GALLERY_IMAGE_LARGE[:GALLERY_IMAGE_LARGE.index('x')],
                     GALLERY_IMAGE_LARGE[GALLERY_IMAGE_LARGE.index('x') + 1:]),
            'box': self.cropping_large,
            'crop': True,
            'detail': True,
        }).url
        return url

    large_image.allow_tags = True

    def small_image(self):
        url = get_thumbnailer(self.image_original).get_thumbnail({
            'size': (GALLERY_IMAGE_SMALL[:GALLERY_IMAGE_SMALL.index('x')],
                     GALLERY_IMAGE_SMALL[GALLERY_IMAGE_SMALL.index('x') + 1:]),
            'box': self.cropping_small,
            'crop': True,
            'detail': True,
        }).url
        return url

    small_image.allow_tags = True

    def medium_image(self):
        url = get_thumbnailer(self.image_original).get_thumbnail({
            'size': (GALLERY_IMAGE_MEDIUM[:GALLERY_IMAGE_MEDIUM.index('x')],
                     GALLERY_IMAGE_MEDIUM[GALLERY_IMAGE_MEDIUM.index('x') + 1:]),
            'box': self.cropping_medium,
            'crop': True,
            'detail': True,
        }).url
        return url

    medium_image.allow_tags = True

    def large_image_admin(self):
        url = get_thumbnailer(self.image_original).get_thumbnail({
            'size': (GALLERY_IMAGE_LARGE[:GALLERY_IMAGE_LARGE.index('x')],
                     GALLERY_IMAGE_LARGE[GALLERY_IMAGE_LARGE.index('x') + 1:]),
            'box': self.cropping_large,
            'crop': True,
            'detail': True,
        }).url
        return str.format('<img src={0} width=100 />', url)

    large_image_admin.allow_tags = True

    def small_image_admin(self):
        url = get_thumbnailer(self.image_original).get_thumbnail({
            'size': (GALLERY_IMAGE_SMALL[:GALLERY_IMAGE_SMALL.index('x')],
                     GALLERY_IMAGE_SMALL[GALLERY_IMAGE_SMALL.index('x') + 1:]),
            'box': self.cropping_small,
            'crop': True,
            'detail': True,
        }).url
        return str.format('<img src={0} width=100 />', url)

    small_image_admin.allow_tags = True

    def medium_image_admin(self):
        url = get_thumbnailer(self.image_original).get_thumbnail({
            'size': (GALLERY_IMAGE_MEDIUM[:GALLERY_IMAGE_MEDIUM.index('x')],
                     GALLERY_IMAGE_MEDIUM[GALLERY_IMAGE_MEDIUM.index('x') + 1:]),
            'box': self.cropping_medium,
            'crop': True,
            'detail': True,
        }).url
        return str.format('<img src={0} width=100 />', url)

    medium_image_admin.allow_tags = True

    class Meta:
        db_table = 'gallery_image_positions'
        verbose_name = _('Gallery Image Position')
        verbose_name_plural = _('Gallery Image Positions')


class BannerImagePosition(models.Model):
    id = models.AutoField(primary_key=True)
    image_original = models.ImageField(_('Original image'),
                                       upload_to=image_directory_path)
    image_small = models.ImageField(_('Small image'),
                                    upload_to=image_directory_path, null=True, blank=True)
    image_medium = models.ImageField(_('Medium image'),
                                     upload_to=image_directory_path, null=True, blank=True)
    image_large = models.ImageField(_('Large image'),
                                    upload_to=image_directory_path, null=True, blank=True)
    name = models.CharField(_('Name'), max_length=256, unique=True)
    title = models.CharField(_('Title'), max_length=256)
    creation_date = models.DateField(_('Date created'), auto_now_add=True, blank=True)
    last_edit_date = models.DateField(_('Date updated'), auto_now=True, blank=True)
    weight = models.IntegerField(_('Weight'))
    active = models.BooleanField(_('Is active?'), default=True)
    description = models.CharField(_('Description'), max_length=256, null=True, blank=True)
    banner = models.ForeignKey('Banner', related_name='banners', verbose_name=_('Banner'))

    image_path = 'image_positions/banners'

    def __str__(self):
        return self.name

    def original_image_admin(self):
        return str.format("<img src=/media/{0} alt='Original Image: {1}' width=100/>", self.image_original, self.title)

    original_image_admin.short_description = _('Original image')
    original_image_admin.allow_tags = True

    def original_image(self):
        return str.format("/media/{0}", self.image_original)

    def large_image(self):
        return str.format("/media/{0}", self.image_large)

    def small_image(self):
        return str.format("/media/{0}", self.image_small)

    def medium_image(self):
        return str.format("/media/{0}", self.image_medium)

    def large_image_admin(self):
        return str.format('<img src=/media/{0} width=100 />', self.image_large)

    large_image_admin.allow_tags = True

    def small_image_admin(self):
        return str.format('<img src=/media/{0} width=100 />', self.image_small)

    small_image_admin.allow_tags = True

    def medium_image_admin(self):
        return str.format('<img src=/media/{0} width=100 />', self.image_medium)

    medium_image_admin.allow_tags = True

    class Meta:
        db_table = 'banner_image_positions'
        verbose_name = _('Banner Image Position')
        verbose_name_plural = _('Banner Image Positions')


class Gallery(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(_('Name'), max_length=256, unique=True)
    creation_date = models.DateField(_('Date created'), auto_now_add=True, blank=True)
    last_edit_date = models.DateField(_('Date updated'), auto_now=True, blank=True)
    first_image = models.ImageField(_('First image'),
                                    upload_to=image_directory_path, null=True, blank=True)
    second_image = models.ImageField(_('Second image'),
                                     upload_to=image_directory_path, null=True, blank=True)

    image_path = "galleries_covers"

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'galleries'
        verbose_name = _('Gallery')
        verbose_name_plural = _('Galleries')

    def first_image_admin(self):
        return str.format("<img src=/media/{0} alt = 'gallery first image', width = 100>", self.first_image)

    first_image_admin.allow_tags = True

    def second_image_admin(self):
        return str.format("<img src=/media/{0} alt = 'gallery second image', width = 100>", self.second_image)

    second_image_admin.allow_tags = True


class Banner(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(_('Name'), max_length=256, unique=True)
    creation_date = models.DateField(_('Date created'), auto_now_add=True, blank=True)
    last_edit_date = models.DateField(_('Date updated'), auto_now=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'banners'
        verbose_name = _('Banner')
        verbose_name_plural = _('Banners')


class Banners:
    def __init__(self):
        self.banners = {}

    def append(self, banner_name, image_positions):
        self.banners[banner_name] = image_positions

    def __getitem__(self, item):
        return self.banners[item]


class GlobalSettings(models.Model):
    company_name = models.CharField(_('Company name'), max_length=255)
    emails = models.TextField(_('Emails'))

    product_title = models.CharField(_('Title for product'), max_length=255,
                                     help_text=_('product title'),
                                     default='<category> <product> - <company>'
                                     )
    product_description = models.CharField(_('Description for product'), max_length=255,
                                           help_text=_('product desc'),
                                           default='<product> <category> <company>'
                                           )
    product_keywords = models.CharField(_('Keywords for product'), max_length=255,
                                        help_text=_('product keywords'),
                                        default='<product>, <company>, <category>'
                                        )

    category_title = models.CharField(_('Title for category'), max_length=255,
                                      help_text=_('category title'),
                                      default='<category> - <company>'
                                      )
    category_description = models.CharField(_('Description for category'), max_length=255,
                                            help_text=_('category desc'),
                                            default='<category> <company>'
                                            )
    category_keywords = models.CharField(_('Keywords for category'), max_length=255,
                                         help_text=_('category keywords'),
                                         default='<company>, <category>'
                                         )

    static_page_title = models.CharField(_('Title for static page'), max_length=255,
                                         help_text=_('static title'),
                                         default='<page_name> - <company>'
                                         )
    static_page_description = models.CharField(_('Description for static page'), max_length=255,
                                               help_text=_('static'),
                                               default='<page_name> <company>'
                                               )
    static_page_keywords = models.CharField(_('Keywords for static page'), max_length=255,
                                            help_text=_('static keys'),
                                            default='<company>, <page_name>'
                                            )
    news_title = models.CharField(_('Title for news'), max_length=255,
                                  help_text=_('news title'),
                                  blank=True)
    news_description = models.CharField(_('Description for news'), max_length=255,
                                        help_text=_('news description'),
                                        blank=True)
    news_keywords = models.CharField(_('Keywords for news'), max_length=255,
                                     help_text=_('news keys'),
                                     blank=True)

    def __str__(self):
        return 'Company: {}, emails: {}'.format(self.company_name, self.emails)

    class Meta:
        verbose_name = _('Global settings')
        verbose_name_plural = _('Global settings')


class Variable(models.Model):
    name = models.SlugField(max_length=255)
    namespace = models.SlugField(max_length=255, default='common')
    value = models.CharField(max_length=255)

    description = models.TextField('Comment', blank=True)

    class Meta:
        unique_together = ('namespace', 'name')
        verbose_name = _('Variable')
        verbose_name_plural = _('Variables')

    def __str__(self):
        return '{} = {}'.format(self.name, self.value)
