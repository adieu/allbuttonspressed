from .models import Post
from django.shortcuts import get_object_or_404
from django.utils.safestring import mark_safe
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list

POSTS_PER_PAGE = 5

def show(request, blog_url, post_url):
    post = get_object_or_404(Post, url='%s/%s' % (blog_url, post_url))

    # To avoid having to always use the "|safe" filter in flatpage templates,
    # mark the title and content as already safe (since they are raw HTML
    # content in the first place).
    post.title = mark_safe(post.title)
    post.content = mark_safe(post.content)

    return direct_to_template(request, 'blog/post_detail.html',
        extra_context={'post': post})

def browse(request, blog_url):
    query = Post.objects.filter(blog=blog_url, published=True)
    query = query.order_by('-published_on')
    return object_list(request, query, paginate_by=POSTS_PER_PAGE)
