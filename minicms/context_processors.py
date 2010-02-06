from .models import Config

def cms(request):
    values = {}

    # Generate menu
    menu = []
    values['menu'] = menu
    try:
        for line in Config.objects.get(pk='menu').content.splitlines():
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
    return values
