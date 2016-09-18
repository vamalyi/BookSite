from django.contrib import admin

from news.models import Post


class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('created_date',)
    list_display = ('__str__', 'status', 'owner', 'created_date')
    list_filter = ('status', 'owner', 'type')
    prepopulated_fields = {'url': ('title',)}

    fieldsets = (
        (None, {
            'fields': ('title', 'url', 'type', 'status', 'body')
        }),
        ('Additional texts', {
            'classes': ('collapse',),
            'fields': ('short_text', 'additional_text'),
        }),
        ('Image', {
            'fields': ('main_image', 'main_image_title', 'main_image_description'),
        }),
        ('SEO content', {
            'classes': ('collapse',),
            'fields': ('meta_title', 'meta_description', 'meta_keywords',
                       'meta_robots', 'meta_canonical', 'h1'),
        }),
        (None, {
            'fields': ('created_date',)
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        if not obj.meta_title:
            obj.meta_title = obj.title
        obj.save()

admin.site.register(Post, PostAdmin)
