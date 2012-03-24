import docutils.core
from blogofile.cache import HierarchicalCache as HC

meta = {
    'name': "reStructuredText",
    'description': "Renders reStructuredText formatted text to HTML",
    }

config = HC(
    aliases = ['rst']
    )

def run(content):
    return docutils.core.publish_parts(
        content, writer_name='html',
        settings_overrides={'initial_header_level': 2}
        )['html_body']
