from django.contrib import admin

from .models import UserData


# Register your models here.

@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'auth_user', "created", "modified"]
    search_fields = ['id', 'auth_user__username', "auth_user__email"]
