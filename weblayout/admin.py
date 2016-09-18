from django.contrib import admin
from genericadmin.admin import GenericAdminModelAdmin, TabularInlineWithGeneric

# Models
from weblayout.models import Template, SystemElement, Menu, MenuItem

# Import / Export
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# MPTT Tree View
from django_mptt_admin.admin import DjangoMpttAdmin


class TemplateResources(resources.ModelResource):
    class Meta:
        model = Template
        fields = ('id', 'name', 'path', 'creation_date', 'last_edit_date', )
        exclude = ('creation_date', 'last_edit_date', )
        export_order = ('id', 'path', 'name', )


class TemplateAdmin(ImportExportModelAdmin):
    resource_class = TemplateResources


class MenuItemInline(TabularInlineWithGeneric):
    fields = ('image', 'content_type', 'object_id', 'alternative_name', 'alternative_url', 'parent', 'menu')
    readonly_fields = ('content_object',)
    model = MenuItem


class MenuItemAdmin(GenericAdminModelAdmin, DjangoMpttAdmin):
    fields = ('image', 'content_type', 'object_id', 'alternative_name', 'alternative_url', 'parent', 'menu')
    readonly_fields = ('content_object',)
    inlines = [MenuItemInline]


class MenuAdmin(GenericAdminModelAdmin):
    inlines = [MenuItemInline]


admin.site.register(Template, TemplateAdmin)
admin.site.register(SystemElement)
admin.site.register(Menu, MenuAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
