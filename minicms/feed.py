# Import Docutils document tree nodes module.
from docutils import nodes
# Import ``directives`` module (contains conversion functions).
from docutils.parsers.rst import directives
# Import Directive base class.
from docutils.parsers.rst import Directive

def align(argument):
    """Conversion function for the "align" option."""
    return directives.choice(argument, ('left', 'center', 'right'))

class Feed(Directive):
    required_arguments = 2
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {'title':directives.unchanged_required, 'align':align,
        'reverse':directives.flag, 'num_results': directives.nonnegative_int}
    has_content = False

    def run(self):
        url = directives.uri(self.arguments[0])
        id = directives.uri(self.arguments[1])
        title = self.options['title']
        reverse = 'reverse' in self.options
        align = self.options.get('align', '')
        num_results = self.options.get('num_results', 50)

        reverse_inner = """result.feed.entries.reverse();
        result.feed.entries = result.feed.entries.slice(0, %s);""" %num_results
        
        code = """
          <!-- ++Begin Dynamic Feed Wizard Generated Code++ -->
          <!--
          // Created with a Google AJAX Search and Feed Wizard
          // http://code.google.com/apis/ajaxsearch/wizards.html
          -->

          <!--
          // The Following div element will end up holding the actual feed control.
          // You can place this anywhere on your page.
          -->
          <div id="%(id)s" class="feed-widget">
            <span style="color:#676767;font-size:11px;margin:10px;padding:4px; %(align)s">Loading...</span>
          </div>

          <!-- Google Ajax Api
          -->
          <script src="http://www.google.com/jsapi?key=notsupplied-wizard"
            type="text/javascript"></script>

          <!-- Dynamic Feed Control and Stylesheet -->
          <script src="http://www.google.com/uds/solutions/dynamicfeed/gfdynamicfeedcontrol.js"
            type="text/javascript"></script>
          <script type="text/javascript">
            /* <![CDATA[ */
            function LoadDynamicFeedControl() {
              var reverse_order = function(result) {
                %(reverse)s
              };
              var feeds = [
                {title: '%(title)s',
                 url: '%(url)s'
                }];
              var options = {
                numResults: %(num_results)s,
                feedLoadCallback: reverse_order
              };

              new GFdynamicFeedControl(feeds, '%(id)s', options);
            };
            // Load the feeds API and set the onload callback.
            google.load('feeds', '1');
            google.setOnLoadCallback(LoadDynamicFeedControl);
            /* ]]> */
          </script>
          <!-- ++End Dynamic Feed Control Wizard Generated Code++ -->
        """ %{'reverse': reverse_inner if reverse else '', 'id':id,
            'title':title, 'url':url, 'align': 'float:%s' %align,
            'num_results': num_results}
        
        feed_node = nodes.raw('', code, format='html')
        return [feed_node]

directives.register_directive('feed', Feed)
