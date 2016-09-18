from django.contrib import admin
from webrating.models import Rating


class RatingAdmin(admin.ModelAdmin):
    list_display = ('date_on_add', 'user_name', 'state', 'comment')

admin.site.register(Rating, RatingAdmin)
