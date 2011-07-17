from django.conf import settings
from django.utils.importlib import import_module
from docutils import core
import os

REST_BACKENDS = getattr(settings, 'REST_BACKENDS', (
    'minicms.markup_highlight',
))

for name in REST_BACKENDS:
    import_module(name).register()

TEMPLATE = os.path.join(os.path.dirname(__file__), 'template.txt')

def html_parts(input_string, source_path=None, destination_path=None,
               input_encoding='unicode', doctitle=1, initial_header_level=2):
    """
    Given an input string, returns a dictionary of HTML document parts.

    Dictionary keys are the names of parts, and values are Unicode strings;
    encoding is up to the client.

    Parameters:

    - `input_string`: A multi-line text string; required.
    - `source_path`: Path to the source file or object.  Optional, but useful
      for diagnostic output (system messages).
    - `destination_path`: Path to the file or object which will receive the
      output; optional.  Used for determining relative paths (stylesheets,
      source links, etc.).
    - `input_encoding`: The encoding of `input_string`.  If it is an encoded
      8-bit string, provide the correct encoding.  If it is a Unicode string,
      use "unicode", the default.
    - `doctitle`: Disable the promotion of a lone top-level section title to
      document title (and subsequent section title to document subtitle
      promotion); enabled by default.
    - `initial_header_level`: The initial level for header elements (e.g. 1
      for "<h1>").
    """
    if not isinstance(input_string, unicode):
        input_string = input_string.decode('utf8')
    overrides = {'input_encoding': input_encoding,
                 'doctitle_xform': doctitle,
                 'embed_stylesheet': False,
                 'template': TEMPLATE,
                 'initial_header_level': initial_header_level}
    parts = core.publish_parts(
        source=input_string, source_path=source_path,
        destination_path=destination_path,
        writer_name='cleanhtmlwriter', settings_overrides=overrides)
    return parts

def html_body(input_string, source_path=None, destination_path=None,
              input_encoding='unicode', output_encoding='unicode',
              doctitle=1, initial_header_level=2):
    """
    Given an input string, returns an HTML fragment as a string.

    The return value is the contents of the <body> element.

    Parameters (see `html_parts()` for the remainder):

    - `output_encoding`: The desired encoding of the output.  If a Unicode
      string is desired, use the default value of "unicode" .
    """
    parts = html_parts(
        input_string=input_string, source_path=source_path,
        destination_path=destination_path,
        input_encoding=input_encoding, doctitle=doctitle,
        initial_header_level=initial_header_level)
    fragment = parts['html_body']
    if output_encoding != 'unicode':
        fragment = fragment.encode(output_encoding)
    return fragment
