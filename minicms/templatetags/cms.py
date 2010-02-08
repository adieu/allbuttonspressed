from ..models import Config
from django.template import Library

register = Library()

@register.simple_tag
def show_block(name):
    try:
        return Config.objects.get(name=name).content
    except Config.DoesNotExist:
        return ''

@register.inclusion_tag('minicms/menu.html', takes_context=True)
def show_menu(context, name='menu'):
    request = context['request']

    menu = []
    try:
        for line in Config.objects.get(name=name).content.splitlines():
            line = line.rstrip()
            try:
                title, url = line.rsplit(' ', 1)
            except:
                continue
            menu.append({'title': title.strip(), 'url': url})
    except Config.DoesNotExist:
        pass

    # Mark the best-matching URL as active
    if request.path != '/':
        import logging
        active = None
        active_len = 0
        # Normalize path
        path = request.path.rstrip('/') + '/'
        for item in menu:
            # Normalize path
            url = item['url'].rstrip('/') + '/'
            if path.startswith(url) and len(url) > active_len:
                active = item
                active_len = len(url)
        if active is not None:
            active['active'] = True
    return {'menu': menu}
