#!/usr/bin/env python
"""Render a directory of blog posts as HTML."""

import os
import re
import utils
from IPython.nbconvert import HTMLExporter
from IPython.nbformat import current as nbformat
from bottle import SimpleTemplate
from datetime import datetime
from docutils.core import publish_doctree
from docutils import nodes
from glob import glob
from jinja2 import DictLoader

from contingent.builderlib import Builder
# from contingent.cachelib import Cache, _absent
from contingent.utils import looping_wait_on

dl = DictLoader({'full.tpl': """\
{%- extends 'display_priority.tpl' -%}
{% block input scoped %}{{ cell.input | highlight2html(language=resources.get('language'), metadata=cell.metadata) }}
{% endblock %}
{% block pyout scoped %}
<pre>
{{ output.text | ansi2html }}
</pre>
{% endblock %}
{% block markdowncell scoped %}{{ cell.source  | markdown2html }}
{% endblock %}
{% block stream_stdout -%}
<pre>
{{ output.text | ansi2html }}
</pre>
{% endblock stream_stdout %}
{% block stream_stderr -%}
<pre>
{{ output.text | ansi2html }}
</pre>
{% endblock stream_stderr %}
{% block data_png scoped %}
{%- if output.png_filename %}
<img src="{{output.png_filename | posix_path}}"
{%- else %}
<img src="data:image/png;base64,{{ output.png }}"
{%- endif %}
{%- if 'metadata' in output and 'width' in output.metadata.get('png', {}) %}
width={{output.metadata['png']['width']}}
{%- endif %}
{%- if 'metadata' in output and 'height' in output.metadata.get('png', {}) %}
height={{output.metadata['png']['height']}}
{%- endif -%}
>
{% endblock data_png %}
"""})

def read_text_file(call, path):
    with open(path) as f:
        return f.read()

def read_binary_file(call, path):
    with open(path, 'rb') as f:
        return f.read()

def parse(call, path):
    source = call(read_text_file, path)
    result = {}
    if path.endswith('.html'):
        if utils.detect_blogofile(source):
            heading, info, other_html = utils.convert_blogofile(source)
            parts = utils.parse_rst(heading)
            body_html = parts['docinfo'] + other_html
            result['title'] = utils.html_parser.unescape(parts['title'])
            result['needs_disqus'] = True
            result['date'] = info['date']
            result['tags'] = info['tags']
        else:
            result['title'] = utils.find_title_in_html(source)
            template = SimpleTemplate(source)
            body_html = template.render() #blog=result['blog'])
            result['needs_disqus'] = False
            result['date'] = None
            result['tags'] = ()

        body_html = utils.pygmentize_pre_blocks(body_html)
        body_html = body_html.replace('\n</pre>', '</pre>')

        result['needs_mathjax'] = False
        result['body'] = body_html
        result['next_link'] = None
        result['previous_link'] = None

    elif path.endswith('.rst'):
        if utils.detect_blogofile(source):
            heading, info, body = utils.convert_blogofile(source)
            source = heading + body

            result['title'] = info['title']
            del heading, info, body
            result['needs_disqus'] = True
        else:
            result['needs_disqus'] = False
        doctree = publish_doctree(source)
        docinfos = doctree.traverse(nodes.docinfo)
        docinfo = {c.tagname: str(c.children[0])
                   for i in docinfos for c in i.children}

        parts = utils.parse_rst(source)
        # parts = publish_from_doctree(source, writer_name='html',
        #                       settings_overrides={'initial_header_level': 2})
        body = parts['docinfo'] + utils.pygmentize_pre_blocks(parts['fragment'])
        result['body'] = body
        result['date'] = datetime.strptime(
            docinfo.get('date'), '%d %B %Y').date()
        if 'title' not in result:
            result['title'] = parts['title']

    elif path.endswith('.ipynb'):
        notebook = nbformat.reads_json(source)
        exporter = HTMLExporter(config=None, extra_loaders=[dl])
        body, resources = exporter.from_notebook_node(notebook)
        body = body.replace('\n</pre>', '</pre>')
        result['body'] = body
        result['date'] = notebook['metadata']['date']
        result['needs_disqus'] = False
        result['title'] = notebook['metadata']['name']

    return result

def title_of(call, path):
    info = call(parse, path)
    return info['title']

def date_of(call, path):
    info = call(parse, path)
    return info['date']

def needs_disqus(call, path):
    info = call(parse, path)
    return info['needs_disqus']

def body_of(call, path):
    info = call(parse, path)
    dirname = os.path.dirname(path)
    body = info['body']
    def format_title_reference(match):
        filename = match.group(1)
        title = title_of(call, os.path.join(dirname, filename))
        return '<i>{}</i>'.format(title)
    body = re.sub(r'title_of\(([^)]+)\)', format_title_reference, body)
    return body

def sorted_posts(call, paths):
    dates = {path: call(date_of, path) for path in paths}
    dated_paths = [path for path in paths if dates[path]]
    return sorted(dated_paths, key=dates.get)

def previous_post(call, paths, path):
    paths = call(sorted_posts, paths)
    i = paths.index(path)
    return paths[i - 1] if i else None

def render(call, paths, path):
    #previous = call(previous_post, paths, path)
    #previous_title = 'NONE' if previous is None else call(title_of, previous)
    body_html = call(body_of, path)
    template = SimpleTemplate(name='layout.html', lookup=['templates'])
    html = template.render(
        add_title='<h1' not in body_html,
        title=call(title_of, path),
        previous_link=None,
        next_link=None,
        body_html=body_html,
        needs_disqus=call(needs_disqus, path),
        needs_mathjax=False, #call(needs_mathjax, path),
        )
    # text = '<h1>{}</h1>\n<p>Date: {}</p>\n<p>Previous post: {}</p>\n{}'.format(
    #     call(title_of, path), call(date_of, path),
    #     previous_title, call(body_of, path))
    # print('-' * 72)
    # print(text)
    return html

def save_text(call, paths, path, outpath):
    text = call(render, paths, path)
    with open(outpath, 'w') as f:
        f.write(text)

def save_static(call, path, outpath):
    data = call(read_binary_file, path)
    with open(outpath, 'wb') as f:
        f.write(data)

class BlogBuilder:
    def __init__(self, verbose=False):
        self.builder = Builder(self.compute)
        self.verbose = verbose

    def get(self, fn, *args):
        return self.builder.get((fn, args))

    def invalidate(self, fn, *args):
        return self.builder.invalidate((fn, args))

    def __getattr__(self, name):
        return getattr(self.builder, name)

    def compute(self, task, _):
        "Compute a task by direct invocation."
        if self.verbose:
            print('Computing', task)

        fn, args = task
        return fn(self.get, *args)

def find(base):
    for dirpath, dirnames, filenames in os.walk(base):
        for filename in filenames:
            yield os.path.join(dirpath, filename)

def main():
    thisdir = os.path.dirname(__file__)
    # indir = os.path.normpath(os.path.join(thisdir, '..', 'texts'))
    outdir = os.path.normpath(os.path.join(thisdir, '..', 'output'))
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    builder = BlogBuilder() #verbose=True)

    text_paths = tuple(
        []
        + glob('texts/brandon/*/*.rst')
        + glob('texts/brandon/*/*.html')
        + glob('texts/brandon/*/*.ipynb')
        + glob('texts/brandon/talks.html')
        )

    for path in text_paths:
        outpath = os.path.join(outdir, path.split('/', 1)[1])
        outpath = os.path.splitext(outpath)[0] + '/index.html'
        os.makedirs(os.path.dirname(outpath), exist_ok=True)
        builder.get(save_text, text_paths, path, outpath)

    static_paths = tuple(find('static'))

    for path in static_paths:
        outpath = os.path.join(outdir, path.split('/', 1)[1])
        os.makedirs(os.path.dirname(outpath), exist_ok=True)
        builder.get(save_static, path, outpath)

    return

    builder.verbose = True
    while True:
        print('=' * 72)
        print('Watching for files to change')
        changed_paths = looping_wait_on(all_paths)
        print('=' * 72)
        print('Reloading:', ' '.join(changed_paths))
        for path in changed_paths:
            builder.invalidate(read_text_file, path)
        builder.rebuild()

if __name__ == '__main__':
    main()
