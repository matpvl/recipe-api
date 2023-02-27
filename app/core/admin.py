"""
Django admin customization.
"""
from django.contrib import admin
# We will call our admin UserAdmin, and we don't want it to conflict with UserAdmin.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from . import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
           _('Permissions'),
           {
               'fields': (
                   'is_active',
                   'is_staff',
                   'is_superuser',
               )
           }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']


admin.site.register(models.User, UserAdmin)
