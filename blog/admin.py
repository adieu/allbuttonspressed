from .models import Blog, Post
from django.contrib import admin
from minicms.admin import BaseAdmin

class BlogAdmin(BaseAdmin):
    list_display = ('title', 'url')
    search_fields = ('url',)
    ordering = ('url',)

class PostAdmin(BaseAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'url', 'blog', 'content', 'published'),
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('author', 'published_on', 'review_key'),
        }),
    )
    list_display = ('title', 'author', 'published_on', 'published')
    search_fields = ('url',)
    ordering = ('-last_update',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()

admin.site.register(Blog, BlogAdmin)
admin.site.register(Post, PostAdmin)
