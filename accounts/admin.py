# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

class UserAdmin(BaseUserAdmin):
    # 定义要显示的字段
    list_display = ('username', 'email', 'is_staff', 'is_active')
    # 定义搜索字段
    search_fields = ('username', 'email')
    # 定义过滤器
    list_filter = ('is_staff', 'is_active')
    # 定义表单字段
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    # 定义添加用户时的表单字段
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

admin.site.register(CustomUser, UserAdmin)