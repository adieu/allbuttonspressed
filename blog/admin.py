from .models import Blog, Post
from django.contrib import admin

class BlogAdmin(admin.ModelAdmin):
    fields = ('base_url', 'title', 'description', 'feed_redirect_url')
    list_display = ('base_url', 'title')
    search_fields = ('base_url',)

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ()
        return ('base_url',)

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
    list_display = ('title', 'url', 'published')
    search_fields = ('url',)
    ordering = ('-published_on',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()

admin.site.register(Blog, BlogAdmin)
admin.site.register(Post, PostAdmin)
