from django import template
from django.conf import settings

register = template.Library()

SHORTNAME = getattr(settings, 'DISQUS_SHORTNAME', None)

def disqus_dev():
    """
    Returns the HTML/js code to enable DISQUS comments on a local 
    development server if the settings.DEBUG is set to True.
    """
    if settings.DEBUG:
        return """
        <script type="text/javascript">
          var disqus_developer = 1;
        </script>
        """
    return ""

def disqus_num_replies():
    """
    Returns the HTML/js code necessary to display the number of comments
    for a DISQUS thread.
    """
    if not SHORTNAME:
        return ''
    return """
    <script type="text/javascript">
    //<![CDATA[
    var disqus_shortname = '%(shortname)s';
    (function () {
      var s = document.createElement('script'); s.async = true;
      s.src = 'http://disqus.com/forums/%(shortname)s/count.js';
      (document.getElementsByTagName('HEAD')[0] || document.getElementsByTagName('BODY')[0]).appendChild(s);
    }());
    //]]>
    </script>
    """ % dict(shortname=SHORTNAME)

def disqus_show_comments():
    """
    Returns the HTML code necessary to display DISQUS comments.
    """
    if not SHORTNAME:
        return ''
    return """
    <div id="disqus_thread"></div>
    <script type="text/javascript">
    //<![CDATA[
      /**
        * var disqus_identifier; [Optional but recommended: Define a unique identifier (e.g. post id or slug) for this thread] 
        */
      (function() {
       var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
       dsq.src = 'http://%(shortname)s.disqus.com/embed.js';
       (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
      })();
    //]]>
    </script>
    <noscript>Please enable JavaScript to view the <a href="http://disqus.com/?ref_noscript=%(shortname)s">comments powered by Disqus.</a></noscript>
    <a href="http://disqus.com" class="dsq-brlink">blog comments powered by <span class="logo-disqus">Disqus</span></a>
    """ % dict(shortname=SHORTNAME)

def disqus_recent_comments(num_items=3, avatar_size=32):
    """
    Returns the HTML/js code necessary to display the recent comments widget.
    """
    if not SHORTNAME:
        return ''
    return """
    <script type="text/javascript" src="http://disqus.com/forums/%(shortname)s/recent_comments_widget.js?num_items=%(num_items)d&amp;avatar_size=%(avatar_size)d"></script>
    <noscript><p><a href="http://%(shortname)s.disqus.com/?url=ref">View the discussion thread.</a></p></noscript>
    """ % dict(shortname=SHORTNAME,
               num_items=num_items,
               avatar_size=avatar_size)

def disqus_popular_threads(num_items=5):
    """
    Returns the HTML/js code necessary to display top commenters
    """
    if not SHORTNAME:
        return ''
    return """
    <script type="text/javascript" src="http://disqus.com/forums/%(shortname)s/popular_threads_widget.js?num_items=%(num_items)d"></script>
    """ % dict(shortname=SHORTNAME,
               num_items=num_items)

register.simple_tag(disqus_dev)
register.simple_tag(disqus_num_replies)
register.simple_tag(disqus_show_comments)
register.simple_tag(disqus_recent_comments)
register.simple_tag(disqus_popular_threads)
