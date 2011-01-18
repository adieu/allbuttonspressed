from .models import Redirect
from django.contrib import admin

class RedirectAdmin(admin.ModelAdmin):
    list_display = ('redirect_from', 'redirect_to')
    search_fields = ('redirect_from',)
    ordering = ('redirect_from',)

admin.site.register(Redirect, RedirectAdmin)
