import re
import sys
import traceback
import logging
from copy import deepcopy

import django
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.utils import six
from django.db.transaction import TransactionManagementError

try:
    from collections import OrderedDict
except ImportError:
    from django.utils.datastructures import SortedDict as OrderedDict

try:
    from django.db.transaction import atomic, savepoint, savepoint_rollback, savepoint_commit  # noqa
except ImportError:
    from import_export.django_compat import atomic, savepoint, savepoint_rollback, savepoint_commit  # noqa

try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text

from import_export.results import Error, Result, RowResult
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.formats import base_formats
from import_export.forms import (
    ImportForm,
    ConfirmImportForm,
    ExportForm,
)

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from image_cropping import ImageCroppingMixin


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdminOld
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.utils.translation import ugettext_lazy as _

from webshop.models import ProductParameterValue, ProductParameter, ProductParameterAvailableValue, ProductReview, \
    ParameterRange, BookSeries, ProductTreeReview
from webshop.models import Product, Category, ProductImagePosition, ProductPriceCorrector, Currency, Provider
from webshop.models import SpecialProposition, PreFilter, DeliveryRule, Margin, Sale, Manufacturer, FastSearch, Author


class ProductParametersInline(admin.TabularInline):
    model = ProductParameterValue


class ProductParameterAvailableValueInline(admin.TabularInline):
    model = ProductParameterAvailableValue
    exclude = ['category']
    show_change_link = True


class ParameterRangeInline(admin.TabularInline):
    model = ParameterRange


class ProductReviewsInline(admin.StackedInline):
    model = ProductTreeReview
    show_change_link = True
    extra = 0


class ProductParametersCategoryInline(admin.TabularInline):
    exclude = ('prefix', 'suffix')
    model = ProductParameter
    show_change_link = True


class ProductParameterResources(resources.ModelResource):
    class Meta:
        model = ProductParameter
        filter = ('id', 'name', 'sort_as', 'category', 'prefix', 'suffix', 'weight',)
        exclude = ('first_image', 'second_image',)
        export_order = ('id', 'category', 'name', 'weight', 'prefix', 'suffix', 'sort_as',)


class ProductParameterAdmin(ImportExportModelAdmin):
    inlines = (ParameterRangeInline, ProductParameterAvailableValueInline)
    list_display = ('name', 'category', 'weight')
    list_editable = ('weight',)
    resource_class = ProductParameterResources


class ProductParameterAvailableValueResources(resources.ModelResource):
    class Meta:
        model = ProductParameterAvailableValue
        filter = ('id', 'product_parameter', 'value', 'weight',)
        exclude = ('first_image', 'second_image',)
        export_order = ('id', 'product_parameter', 'value', 'weight',)


class ProductParameterAvailableValueAdmin(ImportExportModelAdmin):
    resource_class = ProductParameterAvailableValueResources


class ProductInline(admin.TabularInline):
    model = Product
    show_change_link = True
    extra = 0

    exclude = ('first_text', 'second_text', 'h1', 'meta_robots', 'meta_canonical', 'meta_description',
               'sale', 'margin', 'special_proposition', 'meta_title')


class CategoryResources(resources.ModelResource):
    class Meta:
        model = Category
        fields = ('id', 'name', 'url', 'meta_title', 'first_text', 'second_text', 'meta_description', 'meta_canonical',
                  'meta_robots', 'h1', 'template',)
        exclude = ('first_image', 'second_image', 'creation_date', 'last_edit_date', 'first_text', 'second_text',)
        export_order = ('id', 'template', 'name', 'url', 'meta_title', 'h1',
                        'meta_description', 'meta_canonical', 'meta_robots',)


class CategoryInline(admin.TabularInline):
    model = Category.users.through


class CategoryAdmin(ImportExportModelAdmin):
    inlines = (ProductParametersCategoryInline,)
    list_display = ('name', 'url')
    prepopulated_fields = {'url': ('name',)}
    superuser_fields = ('users', 'groups')
    filter_horizontal = ('groups', 'users',)
    resource_class = CategoryResources

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        qs = qs.annotate(user_count=Count('users')).filter(Q(users=request.user) | Q(user_count=0) |
                                                           Q(groups__in=list(request.user.groups.all())))
        return qs

    def has_change_permission(self, request, obj=None):
        perm = super().has_change_permission(request, obj)
        if request.user.is_superuser:
            return True
        if not perm or obj is None:
            return perm
        perm = (not obj.users.exists() or request.user in obj.users.all() or
                obj.groups.filter(user=request.user).exists())
        return perm

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if request.user.is_superuser:
            return fields
        return tuple([f for f in fields if f not in self.superuser_fields])

    class Media:
        js = (
            # 'system/js/admin-transliteration.js',
            'system/js/admin-webshop_category.js',
        )


class ProductImagePositionAdminInline(admin.TabularInline):
    model = ProductImagePosition
    exclude = ('cropping_large', 'cropping_small', 'cropping_medium', 'active', 'description', 'title', 'name')
    extra = 0
    show_change_link = True


class ProductPriceCorrectorInline(admin.TabularInline):
    model = ProductPriceCorrector
    extra = 0


class HasNewCommentsListFilter(admin.SimpleListFilter):
    title = _('Has new comments')
    parameter_name = 'comments_num'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('with_new', _('With new comments')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == 'with_new':
            products_ratings = ProductReview.objects.filter(state=False).all()
            products = []
            for rating in products_ratings:
                products.append(rating.product.id)
            return queryset.filter(id__in=products).all()


class ProductResources(resources.ModelResource):
    class Meta:
        model = Product
        fields = ('id', 'name', 'code', 'url', 'meta_title', 'default_price', 'active', 'first_text', 'second_text',
                  'meta_description', 'meta_canonical', 'meta_robots', 'h1',
                  'special_proposition', 'provider', 'category', 'weight', 'mass',
                  'sale', 'margin', )
        # exclude = ('creation_date', 'last_edit_date', 'first_text', 'second_text', )
        export_order = ('id', 'category', 'provider', 'name', 'code', 'url', 'meta_title',
                        'default_price', 'active', 'weight', 'sale', 'margin',
                        'h1', 'meta_description', 'meta_canonical', 'meta_robots',
                        'mass', 'special_proposition',)

        required_fields = ('name', 'id', 'code', 'url', 'default_price', 'active', 'weight')

    @staticmethod
    def append_raise(e, error_text, row_result):
        if not isinstance(e, TransactionManagementError):
            logging.exception(e)
        tb_info = ''
        row = ''
        row_result.errors.append(Error(error_text, tb_info, row))
        return row_result

    @atomic()
    def import_data(self, dataset, dry_run=False, raise_errors=False,
                    use_transactions=None, **kwargs):
        result = Result()
        result.diff_headers = self.get_diff_headers()

        if use_transactions is None:
            use_transactions = self.get_use_transactions()

        if use_transactions is True:
            real_dry_run = False
            sp1 = savepoint()
        else:
            real_dry_run = dry_run

        try:
            self.before_import(dataset, real_dry_run, **kwargs)
        except Exception as e:
            logging.exception(e)
            tb_info = traceback.format_exc(2)
            result.base_errors.append(Error(repr(e), tb_info))
            if raise_errors:
                if use_transactions:
                    savepoint_rollback(sp1)
                raise

        instance_loader = self._meta.instance_loader_class(self, dataset)

        for row in dataset.dict:
            errors = []
            try:
                row_result = RowResult()

                errors = []

                required_fields = []
                for f in self._meta.required_fields:
                    if row[f] == '':
                        required_fields.append(f)
                if required_fields:
                    errors.append('{} обязательные для заполнения.'.format(', '.join(required_fields)))

                if row['active'] not in ('0', '1'):
                    errors.append('active должен быть равен 1 (активный) или 0 (неактивный).')

                try:
                    if float(row['default_price']) < 0:
                        errors.append('default_price должна быть не меньше нуля.')
                except ValueError:
                    errors.append('default_price должна быть числом не меньше нуля.')

                try:
                    if float(row['weight']) < 0:
                        errors.append('weight должен быть не меньше нуля.')
                except ValueError:
                    errors.append('weight должен быть числом не меньше нуля.')

                try:
                    if row['mass'] != '' and float(row['mass']) < 0:
                        errors.append('mass должен быть не меньше нуля.')
                except ValueError:
                    errors.append('mass должен быть числом не меньше нуля.')

                try:
                    instance, new = self.get_or_init_instance(instance_loader, row)
                    if new:
                        row_result.import_type = RowResult.IMPORT_TYPE_NEW
                    else:
                        row_result.import_type = RowResult.IMPORT_TYPE_UPDATE
                    row_result.new_record = new
                    original = deepcopy(instance)
                    if self.for_delete(row, instance):
                        if new:
                            row_result.import_type = RowResult.IMPORT_TYPE_SKIP
                            row_result.diff = self.get_diff(None, None,
                                                            real_dry_run)
                        else:
                            row_result.import_type = RowResult.IMPORT_TYPE_DELETE
                            self.delete_instance(instance, real_dry_run)
                            row_result.diff = self.get_diff(original, None,
                                                            real_dry_run)
                    else:
                        self.import_obj(instance, row, real_dry_run)
                        if self.skip_row(instance, original):
                            row_result.import_type = RowResult.IMPORT_TYPE_SKIP
                        else:
                            self.save_instance(instance, real_dry_run)
                            self.save_m2m(instance, row, real_dry_run)
                            row_result.object_repr = force_text(instance)
                            row_result.object_id = instance.pk
                        row_result.diff = self.get_diff(original, instance,
                                                        real_dry_run)
                except Category.DoesNotExist:
                    error_text = 'Категория с id {} не существует. Пожалуйста, укажите существующию катерогию.'.format(
                        row['category'])
                    errors.append(error_text)
                except Provider.DoesNotExist:
                    error_text = 'Провайдер с id {} не существует. Пожалуйста, укажите существующего провайдера.'.format(
                        row['provider'])
                    errors.append(error_text)
                except Sale.DoesNotExist:
                    error_text = 'Скидка с id {} не существует. Пожалуйста, укажите существующию скидку .'.format(
                        row['sale'])
                    errors.append(error_text)
                except Margin.DoesNotExist:
                    error_text = 'Наценка с id {} не существует. Пожалуйста, укажите существующию наценку.'.format(
                        row['margin'])
                    errors.append(error_text)
                except SpecialProposition.DoesNotExist:
                    error_text = 'Акция с id {} не существует. Пожалуйста, укажите существующию акцию.'.format(
                        row['special_proposition'])
                    errors.append(error_text)

                if errors:
                    raise ValueError(errors)

            except Exception as e:
                if not isinstance(e, TransactionManagementError):
                    logging.exception(e)
                tb_info = ''
                row = ''
                if errors:
                    error_text = re.findall("'([^']+)'", str(e))
                    for e in error_text:
                        row_result.errors.append(Error(e, tb_info, row))
                else:
                    row_result.errors.append(Error(e, tb_info, row))
                if raise_errors:
                    if use_transactions:
                        savepoint_rollback(sp1)
                    six.reraise(*sys.exc_info())
            if (row_result.import_type != RowResult.IMPORT_TYPE_SKIP or
                    self._meta.report_skipped):
                result.rows.append(row_result)

        if use_transactions:
            if dry_run or result.has_errors():
                savepoint_rollback(sp1)
            else:
                savepoint_commit(sp1)

        return result


class ProductAdmin(ImportExportModelAdmin):
    list_display = ('article', 'name', 'default_price', 'sale', 'active',
                    'is_new', 'is_top', 'is_hit', 'weight')
    prepopulated_fields = {'url': ('name',)}
    inlines = (ProductParametersInline, ProductImagePositionAdminInline)
    search_fields = ('name', 'code', 'article')
    resource_class = ProductResources
    list_filter = ('category', 'series')
    list_display_links = ('article', 'name')
    list_editable = ('active', 'sale', 'is_new', 'is_top', 'is_hit', 'weight', 'default_price')
    actions = ['make_active', 'make_inactive', 'export_selected_objects', 'delete_sale']

    fieldsets = (
        (None, {
            'fields': ('name', 'url', 'code', 'article', 'category', 'authors', 'series', 'weight', 'tags')
        }),
        (_('Prices'), {
            'fields': ('default_price', 'sale',)
        }),
        (_('Statuses'), {
            'fields': ('active', 'is_top', 'is_new', 'is_hit')
        }),
        (_('Description'), {
            'classes': ('collapse',),
            'fields': ('first_text', 'second_text'),
        }),
        (None, {
            'fields': ('mass',),
        }),
        (_('SEO content'), {
            'classes': ('collapse',),
            'fields': ('meta_title', 'meta_description', 'meta_keywords',
                       'meta_robots', 'meta_canonical', 'h1'),
        }),
    )

    formats = (
        base_formats.CSV,
        base_formats.XLSX,
    )

    class Media:
        js = (
            # 'system/js/admin-transliteration.js',
            'system/js/admin-webshop_product.js',
        )

    def make_active(self, request, queryset):
        queryset.update(active=True)
    make_active.short_description = _("Mark selected products as active")

    def make_inactive(self, request, queryset):
        queryset.update(active=False)
    make_inactive.short_description = _("Mark selected products as inactive")

    def export_selected_objects(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        return HttpResponseRedirect(reverse('set_product_sale', kwargs={'pks': ','.join(selected)}))
    export_selected_objects.short_description = 'Установить скидку на выбранный товар'

    def delete_sale(self, request, queryset):
        queryset.update(sale=None)
    delete_sale.short_description = 'Удалить скидку на выбранный товар'

    def export_action(self, request, *args, **kwargs):
        formats = self.get_export_formats()
        form = ExportForm(formats, request.POST or None)
        if form.is_valid():
            file_format = formats[
                int(form.cleaned_data['file_format'])
            ]()

            queryset = self.get_export_queryset(request)
            export_data = self.get_export_data(file_format, queryset)
            content_type = file_format.get_content_type()
            # Django 1.7 uses the content_type kwarg instead of mimetype
            try:
                response = HttpResponse(export_data, content_type=content_type)
            except TypeError:
                response = HttpResponse(export_data, mimetype=content_type)
            response['Content-Disposition'] = 'attachment; filename=%s' % (
                self.get_export_filename(file_format),
            )
            return response

        context = {}

        if django.VERSION >= (1, 8, 0):
            context.update(self.admin_site.each_context(request))
        elif django.VERSION >= (1, 7, 0):
            context.update(self.admin_site.each_context())

        info = {
            'categories': Category.objects.order_by('id'),
            'providers': Provider.objects.order_by('id'),
            'sales': Sale.objects.order_by('id'),
            'margins': Margin.objects.order_by('id'),
            'special_propositions': SpecialProposition.objects.order_by('id'),
        }
        context.update(info)

        context['form'] = form
        context['opts'] = self.model._meta
        return TemplateResponse(request, [self.export_template_name],
                                context, current_app=self.admin_site.name)

    def import_action(self, request, *args, **kwargs):
        '''
        Perform a dry_run of the import to make sure the import will not
        result in errors.  If there where no error, save the user
        uploaded file to a local temp file that will be used by
        'process_import' for the actual import.
        '''
        resource = self.get_import_resource_class()()

        context = {}

        import_formats = self.get_import_formats()
        form = ImportForm(import_formats,
                          request.POST or None,
                          request.FILES or None)

        if request.POST and form.is_valid():
            input_format = import_formats[
                int(form.cleaned_data['input_format'])
            ]()
            import_file = form.cleaned_data['import_file']
            # first always write the uploaded file to disk as it may be a
            # memory file or else based on settings upload handlers
            tmp_storage = self.get_tmp_storage_class()()
            data = bytes()
            for chunk in import_file.chunks():
                data += chunk

            tmp_storage.save(data, input_format.get_read_mode())

            # then read the file, using the proper format-specific mode
            # warning, big files may exceed memory
            try:
                data = tmp_storage.read(input_format.get_read_mode())
                if not input_format.is_binary() and self.from_encoding:
                    data = force_text(data, self.from_encoding)
                dataset = input_format.create_dataset(data)
            except UnicodeDecodeError as e:
                return HttpResponse(_(u"<h1>Imported file is not in unicode: %s</h1>" % e))
            except Exception as e:
                return HttpResponse(_(u"<h1>%s encountred while trying to read file: %s</h1>" % (type(e).__name__, e)))
            result = resource.import_data(dataset, dry_run=True,
                                          raise_errors=False,
                                          file_name=import_file.name,
                                          user=request.user)

            context['result'] = result

            if not result.has_errors():
                context['confirm_form'] = ConfirmImportForm(initial={
                    'import_file_name': tmp_storage.name,
                    'original_file_name': import_file.name,
                    'input_format': form.cleaned_data['input_format'],
                })

        if django.VERSION >= (1, 8, 0):
            context.update(self.admin_site.each_context(request))
        elif django.VERSION >= (1, 7, 0):
            context.update(self.admin_site.each_context())

        info = {
            'categories': Category.objects.order_by('id'),
            'providers': Provider.objects.order_by('id'),
            'sales': Sale.objects.order_by('id'),
            'margins': Margin.objects.order_by('id'),
            'special_propositions': SpecialProposition.objects.order_by('id'),
        }
        context.update(info)

        context['form'] = form
        context['opts'] = self.model._meta
        context['fields'] = [f.column_name for f in resource.get_fields()]

        return TemplateResponse(request, [self.import_template_name],
                                context, current_app=self.admin_site.name)


class PreFilterAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'original_url')


class ProductImageResources(resources.ModelResource):
    class Meta:
        model = ProductImagePosition
        fields = ('id', 'image_original', 'cropping_large', 'cropping_medium', 'cropping_small', 'name', 'title',
                  'creation_date', 'last_edit_date', 'weight', 'active', 'description', 'product',)
        exclude = ('creation_date', 'last_edit_date',)
        export_order = ('id', 'product', 'name', 'image_original', 'cropping_large', 'cropping_medium',
                        'cropping_small', 'title', 'weight', 'active', 'description',)


class ProductImageAdmin(ImageCroppingMixin, ImportExportModelAdmin):
    list_display = ('name', 'creation_date', 'last_edit_date', 'weight', 'active', 'title', 'description',
                    'original_image', 'large_image_admin', 'medium_image_admin', 'small_image_admin')
    fieldsets = (
        (None, {
            'fields': ('name', 'image_original')
        }),
        ('Images', {
            'classes': ('collapse',),
            'fields': ('cropping_large', 'cropping_medium', 'cropping_small'),
        }),
        (None, {
            'fields': ('active', 'weight', 'title', 'description', 'product'),
        }),
    )
    readonly_fields = ('product',)
    # list_filter = ('product',)
    resource_class = ProductImageResources


class ProviderResources(resources.ModelResource):
    class Meta:
        model = Provider
        export_order = ('id', 'currency', 'name', 'coefficient',)


class ProviderAdmin(ImportExportModelAdmin):
    resource_class = ProviderResources


class CurrencyResources(resources.ModelResource):
    class Meta:
        model = Currency


class CurrencyAdmin(ImportExportModelAdmin):
    resource_class = CurrencyResources, ProductTreeReview


class ProductParameterValueResources(resources.ModelResource):
    class Meta:
        model = ProductParameterValue
        fields = ('id', 'product', 'category', 'product_parameter', 'value', 'custom_value',)
        export_order = ('id', 'product', 'category', 'product_parameter', 'value', 'custom_value',)


class ProductParameterValueAdmin(ImportExportModelAdmin):
    resource_class = ProductParameterValueResources


class ProductTreeReviewAdmin(admin.ModelAdmin):
    readonly_fields = ('product', 'user', 'name', 'email', 'body', 'score', 'date_created')
    list_display = ('__str__', 'status', 'user_name', 'score', 'date_created')
    list_editable = ('status',)
    list_filter = ('status',)


class FastSearchAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'value', 'display_order', 'is_published')
    list_editable = ('value', 'display_order', 'is_published')

    list_filter = ('is_published',)
    search_fields = ('value',)
    actions = ['publish', 'unpublish']

    def publish(self, request, queryset):
        queryset.update(is_published=True)
    publish.short_description = _("Mark selected words as published")

    def unpublish(self, request, queryset):
        queryset.update(is_published=False)
    unpublish.short_description = _("Mark selected words as unpublished")


class DeliveryRuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    exclude = ('from_mass', 'to_mass')
    readonly_fields = ('code',)
    list_editable = ('price',)


class ManufacturerAdmin(admin.ModelAdmin):
    exclude = ('slug',)


class AuthorAdmin(admin.ModelAdmin):
    exclude = ('slug',)


class BookSeriesAdmin(admin.ModelAdmin):
    exclude = ('slug',)

admin.site.register(ProductImagePosition, ProductImageAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductParameter, ProductParameterAdmin)
admin.site.register(ProductParameterValue, ProductParameterValueAdmin)
admin.site.register(ProductParameterAvailableValue, ProductParameterAvailableValueAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Provider, ProviderAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SpecialProposition)
admin.site.register(PreFilter, PreFilterAdmin)
admin.site.register(DeliveryRule, DeliveryRuleAdmin)
admin.site.register(Margin)
admin.site.register(Sale)
# admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(BookSeries, BookSeriesAdmin)
admin.site.register(FastSearch, FastSearchAdmin)
admin.site.register(ProductTreeReview, ProductTreeReviewAdmin)
