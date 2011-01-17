from django.conf import settings
from django.db.models.signals import post_init, pre_save, post_save
from django.utils.importlib import import_module

URL_ROUTE_HANDLERS = getattr(settings, 'URL_ROUTE_HANDLERS', ())

handlers = {}

def load_handlers():
    for name in URL_ROUTE_HANDLERS:
        module_name, class_name = name.rsplit('.', 1)
        handler = getattr(import_module(module_name), class_name)()
        add_handler(handler)

def add_handler(handler):
    assert handler.name not in handlers, (
        'An URL handler with the name "%s" already exists!') % handler.name
    handlers[handler.name] = handler

    dispatch_uid = 'urlrouter:%s' % id(handler.model)
    post_init.connect(backup_urls, sender=handler.model,
                      dispatch_uid=dispatch_uid)
    pre_save.connect(reclaim_urls, sender=handler.model,
                     dispatch_uid=dispatch_uid)
    post_save.connect(add_new_urls, sender=handler.model,
                      dispatch_uid=dispatch_uid)

def backup_urls(sender, instance, **kwargs):
    if instance.pk is None:
        instance._urlrouter_urls_backup_ = set()
        return
    urls = set()
    for handler in handlers.values():
        if sender is not handler.model:
            continue
        urls |= set(handler.get_urls(instance))
    instance._urlrouter_urls_backup_ = urls

def reclaim_urls(sender, instance, **kwargs):
    from .models import URLRoute
    reclaim = instance._urlrouter_urls_backup_
    for handler in handlers.values():
        if sender is not handler.model:
            continue
        reclaim -= set(handler.get_urls(instance))
    URLRoute.objects.filter(url__in=reclaim, target=unicode(instance.pk)).delete()
    instance._urlrouter_urls_backup_ -= reclaim

def add_new_urls(sender, instance, **kwargs):
    from .models import URLRoute
    query = URLRoute.objects.filter(url__in=instance._urlrouter_urls_backup_)
    query = query.filter(target=unicode(instance.pk))
    assigned_urls = set(url for url in query)

    add = {}
    for handler in handlers.values():
        if sender is not handler.model:
            continue
        for url in handler.get_urls(instance):
            if url in assigned_urls:
                continue
            assert url not in add, (
                'URL handler "%s" wants to add URL "%s" which was already '
                'added by handler "%s".') % (handle.name, url, add[url])
            add[url] = handler.name
    for url in add:
        URLRoute(url=url, handler=add[url], target=unicode(instance.pk)).save()
    instance._urlrouter_urls_backup_ = assigned_urls | set(add.keys())

load_handlers()
