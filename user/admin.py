from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    model = User

    list_display = (
        'username',
        'first_name',
        'last_name',
        'mobile_number',
        'is_staff',
        'is_active',
    )

    fieldsets = (
        (
            'Authentication',
            {
                'fields': (
                    'username',
                    'password',
                ),
            },
        ),
        (
            'Personal Information',
            {
                'fields': (
                    'first_name',
                    'last_name',
                    'email',
                    'mobile_number',
                    'address',
                ),
            },
        ),
        (
            'Permissions',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                ),
            },
        ),
        (
            'Important Dates',
            {
                'fields': (
                    'last_login',
                    'date_joined',
                ),
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                'classes': (
                    'wide',
                ),
                'fields': (
                    'username',
                    'first_name',
                    'last_name',
                    'email',
                    'mobile_number',
                    'address',
                    'password1',
                    'password2',
                    'is_active',
                    'is_staff',
                ),
            },
        ),
    )