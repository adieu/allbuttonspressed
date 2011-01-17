from .models import Blog, Post
from django.template.loader import render_to_string
from docutils import nodes
from docutils.parsers.rst import directives, Directive

class BlogPosts(Directive):
    required_arguments = 1
    optional_arguments = 0
    option_spec = {'num_results': directives.nonnegative_int,
                   'class': directives.unchanged}
    has_content = False

    def run(self):
        url = directives.uri(self.arguments[0])
        num_results = self.options.get('num_results', 5)
        ul_class = self.options.get('class')

        try:
            blog = Blog.objects.get(url=url)
            recent_posts = Post.objects.filter(blog=blog, published=True)
            recent_posts = recent_posts.order_by('-published_on')[:num_results]
    
            code = render_to_string('blog/recent_posts.html',
                {'recent_posts': recent_posts, 'blog': blog,
                 'recent_posts_class': ul_class})
        except Blog.DoesNotExist:
            code = 'Error: Blog not found: %s' % url

        feed_node = nodes.raw('', code, format='html')
        return [feed_node]

def register():
    directives.register_directive('blogposts', BlogPosts)
