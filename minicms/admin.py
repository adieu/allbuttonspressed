from .models import Page
from django.contrib import admin

class PageAdmin(admin.ModelAdmin):
    list_display = ('url', 'title')
    search_fields = ('url',)

admin.site.register(Page, PageAdmin)
