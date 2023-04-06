from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import MyUser, Subscriptions


class MyUserAdmin(UserAdmin):
    list_display = ('is_active', 'username', 'first_name', 'last_name', 'email')
    fields = (
        ('is_active', ),
        ('username', 'email', ),
        ('first_name', 'last_name', ),
    )
    fieldsets = []
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'first_name', 'email')
    save_on_top = True

admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Subscriptions)