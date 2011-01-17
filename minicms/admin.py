from .models import Block, Page
from django.contrib import admin
from django.contrib.admin.widgets import AdminTextareaWidget
from django.db import models

# The default TextField doesn't have enough rows
class UsableTextarea(AdminTextareaWidget):
    def __init__(self, attrs=None):
        default_attrs = {'rows': '32'}
        if attrs:
            default_attrs.update(attrs)
        super(UsableTextarea, self).__init__(default_attrs)

class BaseAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': UsableTextarea},
    }

class PageAdmin(BaseAdmin):
    fields = ('url', 'title', 'content', 'show_share_buttons')
    list_display = ('url', 'title', 'show_share_buttons')
    search_fields = ('url',)
    ordering = ('url',)

class BlockAdmin(BaseAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

admin.site.register(Page, PageAdmin)
admin.site.register(Block, BlockAdmin)
