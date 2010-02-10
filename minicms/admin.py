from .models import Block, Page
from django.contrib import admin

class PageAdmin(admin.ModelAdmin):
    fields = ('url', 'title', 'content')
    list_display = ('url', 'title')
    search_fields = ('url',)
    ordering = ('url',)

class BlockAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

admin.site.register(Page, PageAdmin)
admin.site.register(Block, BlockAdmin)
