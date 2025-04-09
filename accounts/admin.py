from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from django import forms
from django.utils.translation import gettext_lazy as _
from .models import User
from .forms import CustomUserForm




from unfold.admin import ModelAdmin

class CustomUserAdmin(ModelAdmin, UserAdmin):
    form = CustomUserForm
    list_display = ('email', 'name', 'is_active', 'verified', 'date_joined')
    list_filter = ('is_active', 'verified', 'date_joined')
    search_fields = ('email', 'name')
    ordering = ('-date_joined',)

    
    fieldsets = (
        (_('معلومات المستخدم'), {'fields': ('email', 'name', 'password')}),
        (_('الأدوار والصلاحيات'), {'fields': ( 'is_active', 'is_staff', 'is_superuser', 'verified')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'verified'),
        }),
    )


admin.site.register(User, CustomUserAdmin)






