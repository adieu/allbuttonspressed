from .models import Blog, Post
from django.contrib import admin

class BlogAdmin(admin.ModelAdmin):
    list_display = ('base_url', 'title')
    search_fields = ('base_url',)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'published')
    search_fields = ('url',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()

admin.site.register(Blog, BlogAdmin)
admin.site.register(Post, PostAdmin)
