from django.shortcuts import get_object_or_404

class URLHandler(object):
    """Base class for URL handling backends"""

    # Subclasses should preferrably set this to a static name
    @property
    def name(self):
        return self.__class__.__name__

    model = None

    def dispatch(self, request, target):
        return self.show(request, get_object_or_404(self.model, pk=target))

    def show(self, request, instance):
        raise NotImplementedError('Missing show() method in URLHandler subclass')

    def get_urls(self, instance):
        yield instance.get_absolute_url()
