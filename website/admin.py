from image_cropping import ImageCroppingMixin

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from website.models import GalleryImagePosition, BannerImagePosition, StaticPage, Gallery, Banner
from website.models import Variable, GlobalSettings


class GalleryImageAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('name', 'creation_date', 'last_edit_date', 'weight', 'active', 'title', 'description',
                    'original_image_admin', 'large_image_admin', 'medium_image_admin', 'small_image_admin')
    list_filter = ('gallery',)


class BannerImageAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('name', 'creation_date', 'last_edit_date', 'weight', 'active', 'title', 'description',
                    'original_image_admin', 'large_image_admin', 'medium_image_admin', 'small_image_admin')
    list_filter = ('banner',)


class GalleryImagePositionAdminInline(admin.StackedInline):
    model = GalleryImagePosition
    exclude = ('cropping_large', 'cropping_small', 'cropping_medium',)
    extra = 0
    show_change_link = True


class GalleryAdmin(admin.ModelAdmin):
    list_display = ('name', 'first_image_admin', 'second_image_admin',)
    inlines = (GalleryImagePositionAdminInline,)


class BannerImagePositionAdminInline(admin.StackedInline):
    model = BannerImagePosition
    extra = 0
    show_change_link = True


class BannerAdmin(admin.ModelAdmin):
    inlines = (BannerImagePositionAdminInline,)


class StaticPageAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    prepopulated_fields = {'url': ('name',)}
    fieldsets = (
        (None, {
            'fields': ('name', 'url')
        }),
        ('Texts', {
            'classes': ('collapse',),
            'fields': ('first_text', 'second_text'),
        }),
        (None, {
            'fields': ('gallery', 'template'),
        }),
        ('SEO content', {
            'classes': ('collapse',),
            'fields': ('meta_title', 'meta_description', 'meta_keywords',
                       'meta_robots', 'meta_canonical', 'h1'),
        }),
    )

    class Media:
        js = (
            # 'system/js/admin-transliteration.js',
            'system/js/admin-webshop_staticpage.js',
        )


class VariableAdmin(admin.ModelAdmin):
    fields = ('namespace', ('name', 'value'), 'description')
    list_display = ('__str__', 'namespace', 'name', 'value')
    list_editable = ('namespace', 'name', 'value')
    list_filter = ('namespace',)


class GlobalSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('company_name', 'emails')
        }),
        (_('Product SEO'), {
            # 'classes': ('collapse',),
            'fields': ('product_title', 'product_description', 'product_keywords'),
            'description': 'Use &#60;product&#62;, &#60;category&#62;, &#60;company&#62;'
        }),
        (_('Category SEO'), {
            # 'classes': ('collapse',),
            'fields': ('category_title', 'category_description', 'category_keywords'),
            'description': 'Use &#60;category&#62;, &#60;company&#62;'
        }),
        (_('Static page SEO'), {
            # 'classes': ('collapse',),
            'fields': ('static_page_title', 'static_page_description', 'static_page_keywords'),
            'description': 'Use &#60;page_name&#62;, &#60;company&#62;'
        }),
        ('News SEO', {
            # 'classes': ('collapse',),
            'fields': ('news_title', 'news_description', 'news_keywords'),
            'description': 'Мета теги, которые отображаются на странице со списком новостей.'
        }),
    )


admin.site.register(StaticPage, StaticPageAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(GalleryImagePosition, GalleryImageAdmin)
admin.site.register(BannerImagePosition, BannerImageAdmin)
admin.site.register(Variable, VariableAdmin)
admin.site.register(GlobalSettings, GlobalSettingsAdmin)