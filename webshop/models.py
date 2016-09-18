from decimal import Decimal
from django.conf import settings
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.db import models
from slugify import slugify
from django.utils.translation import pgettext_lazy, ugettext_lazy as _
import re
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.db.models import Sum, Count

# WebLayout models
from core.models import AbstractSeoContent
from utils.fields import NullCharField
from weblayout.models import Template

# Ckeditor support
from ckeditor.fields import RichTextField

# Chained selects support
from smart_selects.db_fields import ChainedForeignKey

# Image cropping support and thumbnails engine
from image_cropping import ImageRatioField
from easy_thumbnails.files import get_thumbnailer
from core.utils import image_directory_path


class ApprovedReviewsManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(status=self.model.APPROVED)


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


def get_default_manufacturer():
    return Manufacturer.objects.get(slug='empty').id if Manufacturer.objects.filter(slug='empty').exists() else 1


def get_default_provider():
    return Provider.objects.get(name='По умолчанию').id if Provider.objects.filter(name='По умолчанию').exists() else 1


class Category(AbstractSeoContent):
    id = models.AutoField(primary_key=True)
    name = models.CharField(pgettext_lazy('category', 'Name'), max_length=256, unique=True)
    url = models.CharField(_('URL'), max_length=256, unique=True)
    first_text = RichTextField(_('First text'), null=True, blank=True)
    second_text = RichTextField(_('Second text'), null=True, blank=True)
    first_image = models.ImageField(_('First image'),
                                    upload_to=image_directory_path, null=True, blank=True)
    second_image = models.ImageField(_('Second image'),
                                     upload_to=image_directory_path, null=True, blank=True)
    template = models.ForeignKey(Template, blank=True, null=True, verbose_name=_('Template'), )
    creation_date = models.DateField(_('Created date'), auto_now_add=True, blank=True)
    last_edit_date = models.DateField(_('Updated date'), auto_now=True, blank=True)

    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='categories', blank=True,
                                   verbose_name=_("Moderators"))
    groups = models.ManyToManyField(Group, verbose_name=_('groups'), blank=True, related_name="categories")

    image_path = "products"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalogue:category_list', kwargs={'category': self.url})

    class Meta:
        db_table = 'categories'
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class ProductImagePosition(models.Model):
    id = models.AutoField(primary_key=True)
    image_original = models.ImageField(_('Original image'),
                                       upload_to=image_directory_path)
    cropping_large = ImageRatioField('image_original', free_crop=True, verbose_name=_('Large image'))
    cropping_medium = ImageRatioField('image_original', free_crop=True, verbose_name=_('Medium image'))
    cropping_small = ImageRatioField('image_original', free_crop=True, verbose_name=_('Small image'))
    image_large = models.CharField(_('Large image'), max_length=256, null=True, blank=True, editable=False)
    image_medium = models.CharField(_('Medium image'), max_length=256, null=True, blank=True, editable=False)
    image_small = models.CharField(_('Small image'), max_length=256, null=True, blank=True, editable=False)
    name = models.CharField(pgettext_lazy('product image item', 'Name'), max_length=256, blank=True)
    title = models.CharField(pgettext_lazy('product image item', 'Title'), max_length=256, null=True, blank=True)
    creation_date = models.DateField(_('Created date'), auto_now_add=True, blank=True)
    last_edit_date = models.DateField(_('Updated date'), auto_now=True, blank=True)
    weight = models.IntegerField(_('Weight'), default=0)
    active = models.BooleanField(_('Is active?'), default=True)
    description = models.CharField(_('Description'), max_length=256, null=True, blank=True)
    product = models.ForeignKey('Product', related_name='images', verbose_name=_('Product'))

    image_path = "image_positions/products"

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(ProductImagePosition, self).save()
        self.image_large = get_thumbnailer(self.image_original).get_thumbnail({
            'size': self.get_new_size(self.cropping_large, settings.PRODUCT_IMAGE_LARGE),
            'box': self.cropping_large,
            'crop': True,
            'detail': True,
        }).url
        self.image_medium = get_thumbnailer(self.image_original).get_thumbnail({
            'size': self.get_new_size(self.cropping_medium, settings.PRODUCT_IMAGE_MEDIUM),
            'box': self.cropping_medium,
            'crop': True,
            'detail': True,
        }).url
        self.image_small = get_thumbnailer(self.image_original).get_thumbnail({
            'size': self.get_new_size(self.cropping_small, settings.PRODUCT_IMAGE_SMALL),
            'box': self.cropping_small,
            'crop': True,
            'detail': True,
        }).url
        super(ProductImagePosition, self).save()

    def original_image(self):
        return str.format("<img src=/media/{0} alt='Original Image: {1}' width=200/>", self.image_original, self.title)

    original_image.short_description = 'Original'
    original_image.allow_tags = True

    @staticmethod
    def get_new_size(crop_size, setting_size):
        crop_size = crop_size.split(',')
        crop_width = int(crop_size[2]) - int(crop_size[0])
        crop_height = int(crop_size[3]) - int(crop_size[1])

        setting_size = setting_size.split('x')
        setting_width = int(setting_size[0])
        setting_height = int(setting_size[1])

        if crop_height / setting_height > crop_width / setting_width:
            result_width = crop_width * setting_height / crop_height
            result_height = setting_height
        else:
            result_width = setting_width
            result_height = crop_height * setting_width / crop_width

        return result_width, result_height

    def large_image(self):
        if self.image_large is None:
            self.save()
        return self.image_large

    large_image.allow_tags = True

    def small_image(self):
        if self.image_small is None:
            self.save()
        return self.image_small

    small_image.allow_tags = True

    def medium_image(self):
        if self.image_medium is None:
            self.save()
        return self.image_medium

    medium_image.allow_tags = True

    def large_image_admin(self):
        url = self.image_large
        return str.format('<img src={0} width=200 />', url)

    large_image_admin.allow_tags = True

    def small_image_admin(self):
        url = self.image_small
        return str.format('<img src={0} width=200 />', url)

    small_image_admin.allow_tags = True

    def medium_image_admin(self):
        url = self.image_medium
        return str.format('<img src={0} width=200 />', url)

    medium_image_admin.allow_tags = True

    class Meta:
        db_table = 'product_image_positions'
        verbose_name = _('Product Image Position')
        verbose_name_plural = _('Product Image Positions')
        unique_together = ('product', 'name')


class Sale(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(pgettext_lazy('sale', 'Name'), max_length=256, unique=True)
    percent = models.FloatField(_('Percent'))
    image = models.ImageField(pgettext_lazy('sale', 'Image'), null=True, blank=True, upload_to=image_directory_path)

    image_path = 'sales'

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sales'
        verbose_name = _('Sale')
        verbose_name_plural = _('Sales')


class Margin(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(pgettext_lazy('margin', 'Name'), max_length=256, unique=True)
    percent = models.FloatField(_('Percent'))

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'margins'
        verbose_name = _('Margin')
        verbose_name_plural = _('Margins')


class DeliveryRule(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(pgettext_lazy('delivery', 'Code'), max_length=256, unique=True, null=True)
    name = models.CharField(pgettext_lazy('delivery', 'Name'), max_length=256, unique=True)
    from_mass = models.FloatField(_('From mass'), null=True, blank=True)
    to_mass = models.FloatField(_('To mass'), null=True, blank=True)
    price = models.DecimalField(pgettext_lazy('delivery', 'Price'), decimal_places=2, max_digits=12,
                                default=Decimal('0.00'))

    class Meta:
        db_table = 'delivery_rules'
        verbose_name = _('Delivery Rule')
        verbose_name_plural = _('Delivery Rules')

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(pgettext_lazy('manufacturer', 'Name'), max_length=256, unique=True)
    slug = models.SlugField(_('Slug'), max_length=256, unique=True, blank=True)

    description = models.TextField(_('Description'), blank=True)
    image = models.ImageField(pgettext_lazy('manufacturer', 'Image'), upload_to=image_directory_path, blank=True,
                              null=True, max_length=255)
    image_path = 'author'

    class Meta:
        ordering = ['name']
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')

    def __str__(self):
        return self.name

    def generate_slug(self):
        return slugify(self.name)

    def ensure_slug_uniqueness(self):
        unique_slug = self.slug
        manufacturers = Manufacturer.objects.exclude(pk=self.pk)
        next_num = 2
        while manufacturers.filter(slug=unique_slug).exists():
            unique_slug = '{slug}_{end}'.format(slug=self.slug, end=next_num)
            next_num += 1

        if unique_slug != self.slug:
            self.slug = unique_slug
            self.save()

    def save(self, *args, **kwargs):
        if self.slug:
            super().save(*args, **kwargs)
        else:
            self.slug = self.generate_slug()
            super().save(*args, **kwargs)
            self.ensure_slug_uniqueness()

    def get_first_letter(self):
        name = self.name
        if re.match('[А-Яа-я]', name.strip()) is not None:
            return 'A-Я'
        if name.strip()[0] in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0'):
            return '0-9'
        return name.strip()[0]


class Author(models.Model):
    name = models.CharField(pgettext_lazy('author', 'Name'), max_length=256, unique=True)
    slug = models.SlugField(_('Slug'), max_length=256, unique=True, blank=True)

    description = models.TextField(_('Description'), blank=True)
    image = models.ImageField(pgettext_lazy('author', 'Image'), upload_to=image_directory_path, blank=True,
                              null=True, max_length=255)
    image_path = 'author'

    class Meta:
        ordering = ['name']
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')

    def __str__(self):
        return self.name

    def generate_slug(self):
        return slugify(self.name)

    def ensure_slug_uniqueness(self):
        unique_slug = self.slug
        authors = Author.objects.exclude(pk=self.pk)
        next_num = 2
        while authors.filter(slug=unique_slug).exists():
            unique_slug = '{slug}_{end}'.format(slug=self.slug, end=next_num)
            next_num += 1

        if unique_slug != self.slug:
            self.slug = unique_slug
            self.save()

    def save(self, *args, **kwargs):
        if self.slug:
            super().save(*args, **kwargs)
        else:
            self.slug = self.generate_slug()
            super().save(*args, **kwargs)
            self.ensure_slug_uniqueness()


class BookSeries(models.Model):
    name = models.CharField(pgettext_lazy('book series', 'Name'), max_length=256, unique=True)
    slug = models.SlugField(_('Slug'), max_length=256, unique=True, blank=True)

    description = models.TextField(_('Description'), blank=True)
    image = models.ImageField(pgettext_lazy('book series', 'Image'), upload_to=image_directory_path, blank=True,
                              null=True, max_length=255)
    image_path = 'series'

    class Meta:
        ordering = ['name']
        verbose_name = _('Series')
        verbose_name_plural = _('Series')

    def __str__(self):
        return self.name

    def generate_slug(self):
        return slugify(self.name)

    def ensure_slug_uniqueness(self):
        unique_slug = self.slug
        series = BookSeries.objects.exclude(pk=self.pk)
        next_num = 2
        while series.filter(slug=unique_slug).exists():
            unique_slug = '{slug}_{end}'.format(slug=self.slug, end=next_num)
            next_num += 1

        if unique_slug != self.slug:
            self.slug = unique_slug
            self.save()

    def save(self, *args, **kwargs):
        if self.slug:
            super().save(*args, **kwargs)
        else:
            self.slug = self.generate_slug()
            super().save(*args, **kwargs)
            self.ensure_slug_uniqueness()

    def get_first_letter(self):
        name = self.name
        if re.match('[А-Яа-я]', name.strip()) is not None:
            return 'A-Я'
        if name.strip()[0] in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0'):
            return '0-9'
        return name.strip()[0]


class Product(AbstractSeoContent):
    name = models.CharField(_('Product name'), max_length=256)
    code = models.CharField(_('ISBN'), max_length=256, unique=True)
    article = NullCharField(_('Article'), max_length=255, unique=True, blank=True, null=True)

    url = models.CharField(_('URL'), max_length=256, unique=True)
    default_price = models.DecimalField(_('Default price of product'), decimal_places=2, max_digits=12)
    active = models.BooleanField(_('Активный товар'), default=True)
    first_text = RichTextField(_('First text'), null=True, blank=True)
    second_text = RichTextField(_('Second text'), null=True, blank=True)
    is_top = models.BooleanField(_('Is top product?'), default=False)
    is_new = models.BooleanField(_('Это новинка?'), default=False)
    is_hit = models.BooleanField(_('It is hit?'), default=False)

    manufacturer = models.ForeignKey(Manufacturer, verbose_name=_('Author'), related_name="products",
                                     blank=True, null=True)
    series = models.ForeignKey(BookSeries, verbose_name=_('Series'), related_name="products",
                               blank=True, null=True)
    authors = models.ManyToManyField(Author, verbose_name=_('Author'), related_name="products")

    date_on_add = models.DateTimeField(_('Last updated date and time'), auto_now=True)

    template = models.ForeignKey(Template, verbose_name=_('Alternative template'), blank=True, null=True)
    special_proposition = models.ForeignKey('SpecialProposition', verbose_name=_('Special proposition'),
                                            null=True, blank=True)
    creation_date = models.DateField(_('Created date'), auto_now_add=True, blank=True)
    last_edit_date = models.DateField(_('Updated date'), auto_now=True, blank=True)
    provider = models.ForeignKey('Provider', verbose_name=_('Provider'), default=get_default_provider)
    category = models.ForeignKey(Category, verbose_name=_('Category'))
    weight = models.IntegerField(_('Weight of product'), default=0, help_text=_('More is good'))
    mass = models.FloatField(_('Mass of product'), default=0)
    sale = models.ForeignKey(Sale, verbose_name=_('Sale'), null=True, blank=True)
    margin = models.ForeignKey(Margin, verbose_name=_('Margin'), null=True, blank=True)

    tags = models.CharField(_('Tags'), max_length=255, blank=True,
                            help_text=_('Введіть теги по яким буде вестись пошук. Теги разділяються комами.'))

    def __str__(self):
        return self.name

    def get_brand(self):
        try:
            return self.manufacturer.name
        except:
            return ''

    def get_absolute_url(self):
        return reverse('catalogue:product_detail', kwargs={'url': self.url})

    def get_delivery_price(self):
        delivery_rules = DeliveryRule.objects.all()
        if delivery_rules:
            for rule in delivery_rules:
                if rule.from_mass is not None and rule.to_mass is not None:
                    if rule.from_mass <= self.mass < rule.to_mass:
                        return rule.price
                elif rule.from_mass is None and rule.to_mass is not None:
                    if self.mass < rule.to_mass:
                        return rule.price
                elif rule.from_mass is not None and rule.to_mass is None:
                    if self.mass >= rule.from_mass:
                        return rule.price
        return 0

    def get_tags_list(self):
        if self.tags:
            return [i.strip() for i in self.tags.split(',')]
        return []

    @property
    def get_approved_reviews(self):
        return ProductTreeReview.approved.filter(product=self)

    @property
    def get_approved_top_reviews(self):
        return ProductTreeReview.approved.filter(product=self, level=0).order_by('-date_created')

    @property
    def get_reviews(self):
        return self.tree_reviews

    def update_rating(self):
        self.rating = self.calculate_rating()
        self.save()

    update_rating.alters_data = True

    def calculate_rating(self):
        result = self.get_reviews.filter(
            status=self.tree_reviews.model.APPROVED
        ).aggregate(
            sum=Sum('score'), count=Count('id'))
        reviews_sum = result['sum'] or 0
        reviews_count = result['count'] or 0
        rating = None
        if reviews_count > 0:
            rating = float(reviews_sum) / reviews_count
        return rating

    @property
    def get_default_price(self):
        coefficient = Decimal('0.00')
        if self.sale:
            coefficient -= self.default_price * Decimal(self.sale.percent / 100)
        if self.margin:
            coefficient += self.default_price * Decimal(self.margin.percent / 100)
        product_price = (self.default_price + coefficient) * Decimal(self.provider.coefficient)
        return product_price.quantize(Decimal('0.01'))

    @property
    def get_default_price_without_sale(self):
        coefficient = Decimal('0.00')
        if self.margin:
            coefficient += self.default_price * Decimal(self.margin.percent / 100)
        product_price = (self.default_price + coefficient) * Decimal(self.provider.coefficient)
        return product_price.quantize(Decimal('0.01'))

    @property
    def price_with_currency(self):
        return '{}: {}'.format(self.provider.currency.short_name, self.get_default_price)

    class Meta:
        db_table = 'products'
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        unique_together = ('name', 'category', 'series')


class ProductTreeReview(MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',
                            verbose_name='Parent menu item')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='tree_reviews', null=True,
                                verbose_name=_('Product'))
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='tree_reviews',
        null=True, blank=True, verbose_name=_('Owner'))
    name = models.CharField(_('Name'), max_length=256, blank=True)
    email = models.CharField(_('Email'), max_length=256, blank=True)

    body = models.TextField(_('Review'))

    SCORE_CHOICES = tuple([(x, x) for x in range(0, 6)])
    score = models.PositiveIntegerField(_('Score'), choices=SCORE_CHOICES, default=0)

    FOR_MODERATION, APPROVED, REJECTED = 0, 1, 2
    STATUS_CHOICES = (
        (FOR_MODERATION, _("Requires moderation")),
        (APPROVED, _("Approved")),
        (REJECTED, _("Rejected")),
    )
    default_status = APPROVED
    if settings.MODERATE_REVIEWS:
        default_status = FOR_MODERATION
    status = models.SmallIntegerField(
        _("Status"), choices=STATUS_CHOICES, default=default_status)

    date_created = models.DateTimeField(_('Date created'), auto_now_add=True, blank=True, null=True)

    # Managers
    objects = models.Manager()
    approved = ApprovedReviewsManager()

    class Meta:
        ordering = ('date_created',)
        verbose_name = _('Product Review')
        verbose_name_plural = _('Product Reviews')

    def __str__(self):
        return '{}: {}/{}'.format(self.product, self.score, self.SCORE_CHOICES[-1][0])

    def user_name(self):
        if self.user:
            return '{} ({})'.format(self.user.username, self.user.email)
        return '{} ({})'.format(self.name, self.email)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.update_rating()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        if self.product is not None:
            self.product.update_rating()


class ProductPriceCorrector(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, verbose_name=_('Product'), related_name='price_correctors')
    name = models.CharField(_('Name of product price corrector'), max_length=256)
    new_price = models.DecimalField(_('Price of corrector'), decimal_places=2, max_digits=12)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('product', 'name')
        db_table = 'product_price_correctors'
        verbose_name = _('Product Price Correction')
        verbose_name_plural = _('Product Price Corrections')

    @property
    def get_new_price(self):
        coefficient = Decimal('0.00')
        if self.product.margin:
            coefficient += self.new_price * Decimal(self.product.margin.percent / 100)
        new_price = self.new_price * Decimal(self.product.provider.coefficient)
        return new_price.quantize(Decimal('0.01'))

    @property
    def get_new_price_with_coefficient(self):
        new_price = self.get_new_price * Decimal(self.product.provider.coefficient)
        coefficient = Decimal('0.00')
        if self.product.sale:
            coefficient -= new_price * Decimal(self.product.sale.percent / 100)
        if self.product.margin:
            coefficient += new_price * Decimal(self.product.margin.percent / 100)
        new_price += coefficient
        return new_price.quantize(Decimal('0.01'))


class ProductReview(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', null=True, verbose_name=_('Product'),
                                on_delete=models.SET_NULL)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='reviews', null=True, blank=True, verbose_name=_('Owner'))
    name = models.CharField(_('Name'), max_length=256, blank=True)
    email = models.CharField(_('Email'), max_length=256, blank=True)

    body = models.TextField(_('Review'))

    SCORE_CHOICES = tuple([(x, x) for x in range(0, 6)])
    score = models.SmallIntegerField(_('Score'), choices=SCORE_CHOICES)

    FOR_MODERATION, APPROVED, REJECTED = 0, 1, 2
    STATUS_CHOICES = (
        (FOR_MODERATION, _("Requires moderation")),
        (APPROVED, _("Approved")),
        (REJECTED, _("Rejected")),
    )
    default_status = APPROVED
    if settings.MODERATE_REVIEWS:
        default_status = FOR_MODERATION
    status = models.SmallIntegerField(
        _("Status"), choices=STATUS_CHOICES, default=default_status)

    date_created = models.DateField(_('Date created'), auto_now=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (('product', 'user'),)
        verbose_name = _('Ratings and comments for product')
        verbose_name_plural = _('Rating and comment for product')


class SpecialProposition(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(_('Special proposition name'), max_length=256, unique=True)
    image = models.ImageField(_('Image of special proposition'), upload_to=image_directory_path, null=True,
                              blank=True)
    image_path = "special_propositions"

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'special_propositions'
        verbose_name = _('Special Proposition')
        verbose_name_plural = _('Special Propositions')


class ProductParameter(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(_('Product parameter name'), max_length=256)
    first_image = models.ImageField(_('First image of parameter'), upload_to=image_directory_path, null=True,
                                    blank=True)
    second_image = models.ImageField(_('Second image of parameter'), upload_to=image_directory_path, null=True,
                                     blank=True)
    category = models.ForeignKey(Category, verbose_name=_('Category'))
    prefix = models.CharField(_('Prefix'), max_length=8, null=True, blank=True)
    suffix = models.CharField(_('Suffix'), max_length=8, null=True, blank=True)
    weight = models.IntegerField(_('Weight of parameter'), default=0)
    image_path = "product_parameter"

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product_parameters'
        ordering = ('category', 'weight')
        verbose_name = _('Product Parameter')
        verbose_name_plural = _('Product Parameters')
        unique_together = ('name', 'category')


class ParameterRange(models.Model):
    name = models.CharField(_('Name of range'), max_length=255)
    weight = models.IntegerField(_('Weight of parameter range'), default=0)
    parameter = models.ForeignKey(ProductParameter, verbose_name=_('Parameter'), related_name='ranges')

    def __str__(self):
        return self.name


class ProductParameterAvailableValue(models.Model):
    id = models.AutoField(primary_key=True)
    product_parameter = models.ForeignKey('ProductParameter', verbose_name=_('Product parameter'),
                                          related_name='values')
    value = models.CharField(_('Value of parameter'), max_length=256)
    first_image = models.ImageField(_('First image'), upload_to=image_directory_path, null=True, blank=True)
    second_image = models.ImageField(_('Second image'), upload_to=image_directory_path, null=True, blank=True)
    weight = models.IntegerField(_('Weight of parameter value'), default=0)

    parameter_range = ChainedForeignKey(ParameterRange, verbose_name=_('Parameter range'), null=True, blank=True,
                                        on_delete=models.SET_NULL,
                                        chained_field="product_parameter",
                                        chained_model_field="parameter",
                                        show_all=False,
                                        related_name='available_values')
    image_path = "product_parameter_value"

    def __str__(self):
        return self.value

    class Meta:
        unique_together = ('product_parameter', 'value')
        db_table = 'product_parameters_available_value'
        verbose_name = _('Product Parameter Available Value')
        verbose_name_plural = _('Product Parameter Available Values')


class ProductParameterValue(models.Model):
    product = models.ForeignKey(Product, related_name='parameter_values', verbose_name=_('Product'))
    category = models.ForeignKey(Category, verbose_name=_('Category'))
    product_parameter = ChainedForeignKey(
        ProductParameter,
        chained_field="category",
        chained_model_field="category",
        show_all=False,
        auto_choose=True,
        related_name='parameter_values',
        verbose_name=_('Product Parameter')
    )
    value = ChainedForeignKey(
        ProductParameterAvailableValue,
        chained_field="product_parameter",
        chained_model_field="product_parameter",
        show_all=False,
        auto_choose=True,
        null=True,
        blank=True,
        related_name='parameter_values',
        verbose_name=_('Value of parameter')
    )

    def __str__(self):
        return str.format("Product: {0} => {1} => {2}",
                          self.product, self.product_parameter, self.value)

    def get_value(self):
        return self.value.value

    class Meta:
        unique_together = ('product', 'category', 'product_parameter', 'value')
        ordering = ('product__weight', 'product_parameter__weight', 'value__weight')
        db_table = 'product_parameters_values'
        verbose_name = _('Product Parameter Value')
        verbose_name_plural = _('Product Parameter Values')


class Currency(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(_('Name of currency'), max_length=256, unique=True)
    short_name = models.CharField(_('Short name of currency'), max_length=3)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'currencies'
        verbose_name = _('Currency')
        verbose_name_plural = _('Currencies')


class Provider(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(_('Name of provider'), max_length=256, unique=True)
    currency = models.ForeignKey(Currency, verbose_name=_('Currency'))
    coefficient = models.FloatField(_('Coefficient to main currency'))

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'providers'
        verbose_name = _('Provider')
        verbose_name_plural = _('Providers')


class PreFilter(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(_('Name of prefilter'), max_length=256, unique=True)
    url = models.CharField(_('URL of prefilter'), max_length=256, unique=True)
    active = models.BooleanField(_('Active?'), default=True)
    first_text = RichTextField(_('First text'), null=True, blank=True)
    second_text = RichTextField(_('Secord text'), null=True, blank=True)
    original_url = models.CharField(_('Original URL'), max_length=1024)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '/catalogue/category/{}/'.format(self.url)

    class Meta:
        db_table = 'pre_filters'
        verbose_name = _('PreFilter')
        verbose_name_plural = _('PreFilters')


class FastSearch(models.Model):
    value = models.CharField(_('Value'), max_length=255, unique=True)
    display_order = models.PositiveSmallIntegerField(
        _('Display order'), default=0,
        help_text=_('Сортування йде від меншого до більшого, числа повинні бути більше нуля'))
    is_published = models.BooleanField(_('Is published?'), default=True)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        verbose_name = _('Word of fast search')
        verbose_name_plural = _('Words of fast search')
        ordering = ('display_order',)

    def __str__(self):
        return self.value
