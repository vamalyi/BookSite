from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from webaccount.models import UserProfile
from webshop.admin import CategoryInline


class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, CategoryInline)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
