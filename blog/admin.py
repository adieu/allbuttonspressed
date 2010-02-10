from .models import Blog, Post
from django.contrib import admin

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'base_url')
    search_fields = ('base_url',)
    ordering = ('base_url',)

class PostAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'blog', 'published'),
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('author', 'url', 'published_on'),
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
