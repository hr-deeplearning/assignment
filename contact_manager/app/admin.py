from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Contact, ContactPhone


class CustomUserAdmin(UserAdmin):
    ordering = ["-id"]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("is_deleted",)}),)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Contact)
admin.site.register(ContactPhone)
