from django.contrib import admin
from .models import Post, User, Like

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    
    list_display = ('user_id', 'email', 'name', 'is_staff', 'is_superuser')

    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_staff', 'is_superuser')
        }),
    )

    
    ordering = ('email',)
    search_fields = ('email', 'name')
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(Post)
admin.site.register(Like)