from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from stack_underflow_app.forms import (CustomUserChangeForm,
                                       CustomUserCreationForm)
from stack_underflow_app.models import PostType, User


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    model = User

    list_display = ('username', 'email', 'is_active',
                    'is_staff', 'is_superuser', 'last_login',)
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        ('General', {'fields': ('username', 'email', 'password', 'dob')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Login and Joining Info', {'fields': ('last_login', 'date_joined')})
    )
    add_fieldsets = (
        (
            None, {
                'classes': ('wide',),
                'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active', 'dob')
            }
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(PostType)
