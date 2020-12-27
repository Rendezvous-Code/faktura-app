from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from core import models
from core.forms import CustomUserProfileModelAdminForm


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'last_name', 'first_name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('first_name', 'last_name')}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


class PermissionGroupAdmin(admin.ModelAdmin):
    filter_horizontal = ['permissions']
    list_display = models.PermissionGroup.ADMIN_DISPLAY


class UserProfileAdmin(admin.ModelAdmin):
    form = CustomUserProfileModelAdminForm
    save_on_top = True
    filter_horizontal = ['permissions', 'group_permisions', "account"]
    list_display = models.UserProfile.ADMIN_DISPLAY


admin.site.register(models.User, UserAdmin)
admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(models.PermissionGroup, PermissionGroupAdmin)
admin.site.register(models.Account,
                    list_display=models.Account.ADMIN_DISPLAY)
admin.site.register(models.Permission,
                    list_display=models.Permission.ADMIN_DISPLAY)
