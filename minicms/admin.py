from .models import Config, Page
from django.contrib import admin

class PageAdmin(admin.ModelAdmin):
    list_display = ('url', 'title')
    search_fields = ('url',)

class ConfigAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Page, PageAdmin)
admin.site.register(Config, ConfigAdmin)
