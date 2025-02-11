from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('More Fields', {'fields': ('role','authCode')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('More Fields', {'fields': ('role','authCode')}),
    )

    list_display = ('username', 'email', 'role','authCode', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'role','authCode')

admin.site.register(CustomUser, CustomUserAdmin)
