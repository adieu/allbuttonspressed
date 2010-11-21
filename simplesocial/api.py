from django.conf import settings
from django.utils.html import escape
from django.utils.http import urlquote
from mediagenerator.utils import media_url

WIDE_TWITTER_BUTTON = """
<iframe src="http://platform.twitter.com/widgets/tweet_button.html?count=horizontal&amp;lang=en&amp;text=%(title)s&amp;url=%(url)s%(opttwitteruser)s" style="float: left; width: 110px; height: 20px; margin-right: 10px;" frameborder="0" scrolling="no"></iframe>
"""

FACEBOOK_LIKE_BUTTON = """
<iframe src="http://www.facebook.com/plugins/like.php?href=%(url)s&amp;layout=standard&amp;show_faces=false&amp;width=280&amp;action=like&amp;colorscheme=light" frameborder="0" scrolling="no" style="border:none; overflow:hidden; width:280px; height: 30px; align: left; margin: 0px 0px 0px 0px;"></iframe>
"""

BASE_BUTTON = '<a class="simplesocial" target="_blank" title="%(title)s" style="margin-right:5px;" href="%(url)s"><img src="%(icon)s" alt="%(title)s" width="32" height="32" /></a>'

DEFAULT_TITLE = 'Share on %s'

NARROW_BUTTONS = {
    'Twitter': {
        'title': 'Tweet this!',
        'url': 'http://twitter.com/share?text=%(title)s&url=%(url)s%(opttwitteruser)s',
    },
    'Facebook': 'http://www.facebook.com/share.php?u=%(url)s&t=%(title)s',
    'Email': {
        'title': 'Email a friend',
        'url': 'http://feedburner.google.com/fb/a/emailFlare?itemTitle=%(title)s&uri=%(url)s',
    },
    'Delicious': 'http://del.icio.us/post?url=%(url)s&title=%(title)s',
    'Digg': 'http://digg.com/submit?url=%(url)s&title=%(title)s',
    'StumbleUpon': 'http://www.stumbleupon.com/submit?url=%(url)s&title=%(title)s',
    'Reddit': 'http://reddit.com/submit?url=%(url)s&title=%(title)s',
    'Technorati': 'http://technorati.com/faves?sub=favthis&add=%(url)s',
}

SHOW_SOCIAL_BUTTONS = getattr(settings, 'SHOW_SOCIAL_BUTTONS',
    ('Twitter', 'Facebook', 'Email', 'Delicious', 'StumbleUpon',
     'Digg', 'Reddit', 'Technorati'))

WIDE_BUTTONS_DIV = '<div class="wide-share-buttons" style="overflow:hidden">%s</div>'
NARROW_BUTTONS_DIV = '<div class="narrow-share-buttons" style="overflow:hidden">%s</div>'

def narrow_buttons(request, title, url, buttons=SHOW_SOCIAL_BUTTONS):
    data = _get_url_data(request, title, url)
    code = []
    for name in buttons:
        button = NARROW_BUTTONS[name]
        if not isinstance(button, dict):
            button = {'url': button}
        title = escape(button.get('title', DEFAULT_TITLE % name))
        url = escape(button['url'] % data)
        icon = escape(button.get('icon',
                                 media_url('simplesocial/icons32/%s.png'
                                           % name.lower())))
        code.append(BASE_BUTTON % {'title': title, 'url': url, 'icon': icon})
    return NARROW_BUTTONS_DIV % '\n'.join(code)

def wide_buttons(request, title, url,
                 buttons=(WIDE_TWITTER_BUTTON, FACEBOOK_LIKE_BUTTON)):
    data = _get_url_data(request, title, url)
    data['opttwitteruser'] = escape(data['opttwitteruser'])
    code = [button % data for button in buttons]
    return WIDE_BUTTONS_DIV % '\n'.join(code)

def _get_url_data(request, title, url):
    url = 'http%s://%s%s' % ('s' if request.is_secure() else '',
                             request.get_host(), url)
    data = {'url': url, 'title': title, 'opttwitteruser': ''}
    twitter_username = getattr(settings, 'TWITTER_USERNAME', None)
    if twitter_username:
        data['opttwitteruser'] = twitter_username
    for key in data:
        data[key] = urlquote(data[key])
    if twitter_username:
        data['opttwitteruser'] = '&via=' + data['opttwitteruser']
    return data
