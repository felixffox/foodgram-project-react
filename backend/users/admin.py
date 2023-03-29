from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import MyUser, Subscriptions


class MyUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email')
    fields = (
        ('username', 'email', ),
        ('first_name', 'last_name', ),
    )
    search_fields = ('username', 'email')
    list_filter = ('first_name', 'email')
    save_on_top = True

admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Subscriptions)