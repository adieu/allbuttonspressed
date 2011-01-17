import re

_NORMALIZE = re.compile(r'\W+', re.UNICODE)

def slugify(text):
    """A unicode-aware alternative to Django's slugify"""
    return _NORMALIZE.sub('-', text.lower()).strip('-')
