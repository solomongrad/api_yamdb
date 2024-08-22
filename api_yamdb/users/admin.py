from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Класс настройки админ зоны пользователей."""

    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role'
    )
    list_editable = ('role',)
    search_fields = ('username',)
    list_display_links = ('username',)
    BaseUserAdmin.fieldsets += (
        ('Extra Fields', {'fields': ('bio', 'role')}),
    )
