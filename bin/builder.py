#!/usr/bin/env python
"""Render a directory of blog posts as HTML."""

import os
import re
import sys
import utils
import nbformat.v4 as nbformat
from CommonMark import commonmark
from nbconvert import HTMLExporter
from bottle import SimpleTemplate
from datetime import datetime
from docutils.core import publish_doctree
from docutils import nodes
from glob import glob
from jinja2 import DictLoader

from contingent.projectlib import Project
# from contingent.cachelib import Cache, _absent
from contingent.io import looping_wait_on

project = Project()

def fixdollars(string):
    while '$$' in string:
        string = string.replace('$$', r'\[', 1)
        string = string.replace('$$', r'\]', 1)
    string = string.replace(r'\$', 'PUT A REAL DOLLAR SIGN HERE')
    while '$' in string:
        string = string.replace('$', r'\(', 1)
        string = string.replace('$', r'\)', 1)
    string = string.replace('PUT A REAL DOLLAR SIGN HERE', '$')
    return string

filters = {'fixdollars': fixdollars}

dl = DictLoader({'brandon.tpl': """\
{%- extends 'display_priority.tpl' -%}
{% block input scoped %}{{ cell.source | highlight2html(language=resources.get('language'), metadata=cell.metadata) }}
{% endblock %}
{% block pyout scoped %}
<pre class="output">
{{ output.text | ansi2html }}
</pre>
{% endblock %}
{% block markdowncell scoped %}{{ cell.source  | markdown2html | fixdollars }}
{% endblock %}
{% block stream_stdout -%}
<pre class="output">
{{ output.text | ansi2html }}
</pre>
{% endblock stream_stdout %}
{% block stream_stderr -%}
<pre class="output">
{{ output.text | ansi2html }}
</pre>
{% endblock stream_stderr %}
{% block data_png scoped %}
{%- if output.png_filename %}
<img src="{{output.png_filename | posix_path}}"
{%- else %}
<img src="data:image/png;base64,{{ output.data['image/png'] }}"
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

@project.task
def read_text_file(path):
    with open(path) as f:
        return f.read()

@project.task
def read_binary_file(path):
    with open(path, 'rb') as f:
        return f.read()

@project.task
def parse(path):
    source = read_text_file(path)
    result = {}
    if path.endswith('.html'):
        if utils.detect_blogofile(source):
            heading, info, other_html = utils.convert_blogofile(source)
            parts = utils.parse_rst(heading)
            body_html = parts['docinfo'] + other_html
            body_html = utils.pygmentize_pre_blocks(body_html)
            body_html = body_html.replace('\n</pre>', '</pre>')
            result['title'] = utils.html_parser.unescape(parts['title'])
            result['needs_disqus'] = True
            result['date'] = info['date']
            result['tags'] = info['tags']
        else:
            result['title'] = utils.find_title_in_html(source)
            body_html = SimpleTemplate(source)
            result['needs_disqus'] = False
            result['date'] = None
            result['tags'] = ()

        result['body'] = body_html
        result['next_link'] = None
        result['previous_link'] = None

    elif path.endswith('.md'):
        if utils.detect_blogofile(source):
            heading, info, body = utils.convert_blogofile(source)
            source = body
            result['date'] = info['date']
            result['title'] = info['title']
            result['needs_disqus'] = True
        else:
            result['needs_disqus'] = False
        result['body'] = commonmark(source)

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
        notebook = nbformat.reads(source)
        docinfo = utils.build_docinfo_block_for_notebook(notebook)
        exporter = HTMLExporter(config=None, extra_loaders=[dl],
                                filters=filters)
        exporter.template_file = 'brandon.tpl'
        #notebook = nbformat.convert(notebook, nbformat.current_nbformat)
        body, resources = exporter.from_notebook_node(notebook)
        body = body.replace('\n</pre>', '</pre>')
        body = body.replace('</h1>', '</h1>\n' + docinfo.rstrip())

        date = notebook['metadata']['date']
        if date is not None:
            date = datetime.strptime(date, '%d %B %Y').date()

        result['body'] = body
        result['date'] = date
        result['needs_disqus'] = notebook['metadata'].get('needs_disqus')
        result['title'] = (notebook['metadata'].get('name', None)
                           or utils.find_title_in_html(body))

    else:
        raise ValueError('unrecognized path: {}'.format(path))

    return result

@project.task
def url_of(path):
    if path.startswith('texts/'):
        path = path[5:]
    if path.endswith('index.html'):
        path = path[:-10]
    else:
        path = path.rsplit('.', 1)[0] + '/'
    return path

@project.task
def title_of(path):
    info = parse(path)
    return info['title']

@project.task
def date_of(path):
    info = parse(path)
    return info['date']

@project.task
def needs_disqus(path):
    info = parse(path)
    return info['needs_disqus']

@project.task
def body_of(path):
    info = parse(path)
    dirname = os.path.dirname(path)
    body = info['body']

    if isinstance(body, SimpleTemplate):
        body = body.render(**globals())
        body = utils.pygmentize_pre_blocks(body)
        body = body.replace('\n</pre>', '</pre>')

    def format_title_reference(match):
        filename = match.group(1)
        title = title_of(os.path.join(dirname, filename))
        return '<i>{}</i>'.format(title)

    body = re.sub(r'title_of\(([^)]+)\)', format_title_reference, body)

    return body

@project.task
def preview_body_of(path):
    body = body_of(path)

    if '<table class="docinfo"' in body:
        i = body.find('</table>') + len('</table>')
    else:
        i = body.find('</h1>') + len('</h1>')

    preview = ''
    preview_limit = 256

    while len(preview) < preview_limit and i < len(body):
        j = body.find('<', i)
        preview += body[i:j]
        i = body.find('>', j) + 1

    j = preview.find(' ', preview_limit)
    if j != -1:
        preview = preview[:j]

    return preview.strip() + u'…'

@project.task
def sorted_posts(paths):
    dates = {path: date_of(path) for path in paths}
    dated_paths = [path for path in paths if dates[path]]
    return sorted(dated_paths, key=dates.get)

@project.task
def most_recent_posts(paths, n):
    paths = sorted_posts(paths)
    i = len(paths) - n
    paths = list(reversed(paths[i:]))
    return paths

@project.task
def previous_post(paths, path):
    paths = sorted_posts(paths)
    i = paths.index(path)
    return paths[i - 1] if i else None

@project.task
def render(paths, path):
    #previous = call(previous_post, paths, path)
    #previous_title = 'NONE' if previous is None else call(title_of, previous)
    body_html = body_of(path)
    template = SimpleTemplate(name='layout.html', lookup=['templates'])
    html = template.render(
        add_title='<h1' not in body_html,
        title=title_of(path),
        previous_link=None,
        next_link=None,
        body_html=body_html,
        needs_disqus=needs_disqus(path),
        needs_mathjax=r'\(' in body_html or r'\[' in body_html,
        )
    # text = '<h1>{}</h1>\n<p>Date: {}</p>\n<p>Previous post: {}</p>\n{}'.format(
    #     call(title_of, path), call(date_of, path),
    #     previous_title, call(body_of, path))
    # print('-' * 72)
    # print(text)
    return html

@project.task
def save_text(paths, path, outpath):
    text = render(paths, path)
    with open(outpath, 'w') as f:
        f.write(text)

@project.task
def save_static(path, outpath):
    data = read_binary_file(path)
    with open(outpath, 'wb') as f:
        f.write(data)

# class BlogBuilder:
#     def __init__(self, verbose=False):
#         self.builder = Builder(self.compute)
#         self.verbose = verbose

#     def get(self, fn, *args):
#         return self.builder.get((fn, args))

#     def invalidate(self, fn, *args):
#         return self.builder.invalidate((fn, args))

#     def __getattr__(self, name):
#         return getattr(self.builder, name)

#     def compute(self, task, _):
#         "Compute a task by direct invocation."
#         if self.verbose:
#             print('Computing', task)

#         fn, args = task
#         return fn(self.get, *args)

def find(base):
    for dirpath, dirnames, filenames in os.walk(base):
        for filename in filenames:
            yield os.path.join(dirpath, filename)

def main():
    global text_paths

    thisdir = os.path.dirname(__file__)
    # indir = os.path.normpath(os.path.join(thisdir, '..', 'texts'))
    outdir = os.path.normpath(os.path.join(thisdir, '..', 'output'))
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    text_paths = tuple(
        []
        + glob('texts/brandon/*/*.md')
        + glob('texts/brandon/*/*.rst')
        + glob('texts/brandon/*/*.html')
        + glob('texts/brandon/*/*.ipynb')
        + glob('texts/brandon/*.html')
        )

    for path in text_paths:
        outpath = os.path.join(outdir, path.split('/', 1)[1])
        if not path.endswith('/index.html'):
            outpath = os.path.splitext(outpath)[0] + '/index.html'
        os.makedirs(os.path.dirname(outpath), exist_ok=True)
        save_text(text_paths, path, outpath)

    static_paths = tuple(find('static'))

    for path in static_paths:
        outpath = os.path.join(outdir, path.split('/', 1)[1])
        os.makedirs(os.path.dirname(outpath), exist_ok=True)
        save_static(path, outpath)

    #return

    all_paths = text_paths + static_paths
    project.verbose = True

    if len(sys.argv) > 1:
        return

    while True:
        print('=' * 72)
        print('Watching for files to change')
        changed_paths = looping_wait_on(all_paths)
        print('=' * 72)
        print('Reloading:', ' '.join(changed_paths))
        for path in changed_paths:
            project.invalidate((read_text_file, (path,)))
        project.rebuild()

if __name__ == '__main__':
    main()
