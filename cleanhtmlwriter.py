from docutils.writers import html4css1

class Writer(html4css1.Writer):
    def __init__(self, *args, **kwargs):
        html4css1.Writer.__init__(self, *args, **kwargs)
        self.translator_class = HTMLTranslator

class HTMLTranslator(html4css1.HTMLTranslator):
    def starttag(self, node, tagname, *args, **kwargs):
        tagname = 'code' if tagname.lower() == 'tt' else tagname
        return html4css1.HTMLTranslator.starttag(self, node, tagname, *args, **kwargs)
