"""Build process powered by `contingent`."""

import os
import re
import sys
import yaml

from bottle import SimpleTemplate
from builderlib import Builder
from collections import defaultdict
from datetime import datetime
from docutils.core import publish_parts
from glob import glob
from html.parser import HTMLParser
from io import StringIO
from operator import attrgetter
from pprint import pprint

from IPython.config import Config
from IPython.nbconvert import HTMLExporter
from IPython.nbformat import current as nbformat

from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter

import magic
import my_feed_builder

html_parser = HTMLParser()


class Blog(magic.Base):
    def __init__(self, builder, fs):
        self._builder = builder
        self._fs = fs
        self.documents = []

    def __repr__(self):
        return '<Blog>'

    def copy_statics(self):
        for path in self.statics:
            self.copy_static(path)

    def copy_static(self, path):
        assert path.startswith('static/')
        output_path = 'output' + path[6:]
        print('Copying', output_path)
        data = self._fs.read(path, 'rb')
        outdir = os.path.dirname(output_path)
        if not os.path.isdir(outdir):
            os.makedirs(outdir)
        with open(output_path, 'wb') as f:
            f.write(data)

    def sorted_posts(self):
        print('Re-sorting posts')
        posts = (document for document in self.documents
                 if (document.date is not None) and document.tags)
        return sorted(posts, key=attrgetter('date', 'title'))

    def most_recent_posts(self, n=7):
        sorted_posts = self.sorted_posts()
        sorted_posts.reverse()
        return sorted_posts[:n]

    def posts_by_tag(self):
        print('PBT')
        groups = defaultdict(list)
        for post in self.sorted_posts():
            for tag in post.tags:
                groups[tag].append(post)
        return groups

    def tags(self):
        return set(self.posts_by_tag())

    def posts_for_tag(self, tag):
        return self.posts_by_tag()[tag]

    def render_feeds(self):
        for tag in self.tags():
            self.render_feed(tag)

    def render_feed(self, tag):
        output_path = 'output/brandon/category/{}/feed/index.xml'.format(tag)
        print('Rendering', output_path)
        html = my_feed_builder.render_feed(tag, self.posts_for_tag(tag))
        outdir = os.path.dirname(output_path)
        if not os.path.isdir(outdir):
            os.makedirs(outdir)
        with create_file(output_path, binary=True) as f:
            f.write(html)


class Document(magic.Base):

    def __init__(self, builder, fs, blog, source_path, output_path):
        self._builder = builder
        self._fs = fs
        self.blog = blog
        self.date = None
        self.source_path = source_path
        self.output_path = output_path
        self.url_path = (output_path.replace('output', '')
                                    .replace('index.html', ''))

    def __repr__(self):
        return '<Document {!r}>'.format(self.source_path.split('/')[-1])

    def _report(self, verb):
        print(verb.title(), self.source_path)

    # def _load(self):
    #     #self._report('loading')
    #     with open(self.source_path, encoding='utf-8') as f:
    #         self.source = f.read()

    def parse(self):
        self._report('parsing')
        self.source = self._fs.read(self.source_path)
        ext = self.source_path.rsplit('.', 1)[1]
        _parse_method = getattr(self, '_parse_' + ext)
        _parse_method()

    def _parse_html(self):
        source = self.source
        if detect_blogofile(source):
            heading, info, other_html = convert_blogofile(source)
            parts = parse_rst(heading)
            body_html = parts['docinfo'] + other_html
            self.add_title = True
            self.title = html_parser.unescape(parts['title'])
            self.add_disqus = True
            self.date = info['date']
            self.tags = info['tags']
        else:
            self.title = self._find_title_in_html(source)
            template = SimpleTemplate(source)
            body_html = template.render(blog=self.blog)
            self.add_disqus = False
            self.date = None
            self.tags = ()
            self.add_title = False

        body_html = pygmentize_pre_blocks(body_html)
        body_html = body_html.replace('\n</pre>', '</pre>')

        self.add_mathjax = False
        self.body_html = body_html
        self.next_link = None
        self.previous_link = None

    def _parse_ipynb(self):
        notebook = nbformat.reads_json(self.source)

        config = Config({'HTMLExporter': {'default_template': 'basic'}})
        exporter = HTMLExporter(config=config)
        body, resources = exporter.from_notebook_node(notebook)

        body = body[body.index('\n<div class="cell'):-36]  # excise template
        body = self._decapitate(body)
        body = body.replace('\n</pre>', '</pre>')

        self.add_mathjax = r'\(' in body

        fields = notebook['metadata']

        if 'date' in fields:
            self.date = datetime.strptime(fields['date'], '%d %B %Y').date()
        else:
            self.date = datetime.now().date()
        self.tags = set()
        if 'tags' in fields:
            self.tags.update('-'.join(tag.strip().lower().split())
                             for tag in fields['tags'].split(','))

        if self.date and self.tags:
            heading = ':Date: {}\n:Tags: {}\n'.format(
                self.date.strftime('%d %B %Y').lstrip('0'),
                ', '.join(sorted(self.tags)),
                )
            parts = parse_rst(heading)
            body = parts['docinfo'] + body

        self.add_disqus = fields.get('add_disqus', False)
        self.body_html = body
        self.next_link = None
        self.previous_link = None
        self.add_title = True

    def _parse_rst(self):
        source = self.source
        if detect_blogofile(source):
            heading, info, body = convert_blogofile(source)
            source = heading + body
            self.add_disqus = True
            self.add_mathjax = info['add_mathjax']
        else:
            self.add_disqus = False
            self.add_mathjax = False

        field_matches = re.findall(r'\n:([^:]+): +(.*)', source)
        fields = {name.lower(): value for name, value in field_matches}

        if 'date' in fields:
            self.date = datetime.strptime(fields['date'], '%d %B %Y').date()
            self.tags = ['-'.join(phrase.strip().lower().split())
                         for phrase in fields['tags'].split(',')]
        else:
            self.date = None
            self.tags = []

        parts = parse_rst(source)
        body_html = parts['docinfo'] + parts['fragment']
        body_html = pygmentize_pre_blocks(body_html)
        body_html = body_html.replace('\n</pre>', '</pre>')

        self.body_html = body_html
        self.next_link = None
        self.previous_link = None
        self.title = html_parser.unescape(parts['title'])
        self.add_title = True

    def _decapitate(self, body):
        pieces = re.split(r'<h1[^>]*>([^>]*)</h1>', body)
        if len(pieces) == 3:
            before, title, after = pieces
            body = before + after
            self.title = html_parser.unescape(title)
        else:
            self.title = ''
        return body

    def _find_title_in_html(self, html):
        pieces = re.split(r'<h1[^>]*>([^>]*)</h1>', html)
        if len(pieces) == 3:
            before, title, after = pieces
            return html_parser.unescape(title)
        else:
            return None

    def render(self):
        self._report('rendering')
        template = SimpleTemplate(name='layout.html', lookup=['templates'])
        html = template.render(post=self)
        with create_file(self.output_path) as f:
            f.write(html)


def create_file(path, binary=False):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if binary:
        return open(path, 'wb')
    else:
        return open(path, 'w', encoding='utf-8')

def parse_rst(source):
    return publish_parts(source, writer_name='html',
                         settings_overrides={'initial_header_level': 2})


def pygmentize_pre_blocks(html):
    formatter = HtmlFormatter()

    def _highlight(match):
        code = match.group(2).strip('\n')
        already_marked_up = '<' in code
        if already_marked_up:
            return u'<pre{}>{}</pre>'.format(match.group(1), code)
        code = html_parser.unescape(code)
        if code.startswith('#!'):
            lexer_name, code = code[2:].split('\n', 1)
            lexer = get_lexer_by_name(lexer_name)
        else:
            lexer = guess_lexer(code)
        return highlight(code, lexer, formatter)

    return re.sub(r'(?s)<pre([^>]*)>(.*?)</pre>', _highlight, html)


def detect_blogofile(source):
    """Does the document start with an old blogofile header?"""

    return source.startswith('---')

def convert_blogofile(source):
    """Replace an old blogofile header with a modern RST title and fields."""

    empty_string, yaml_text, body = source.split('---', 2)
    yams = yaml.load(StringIO(yaml_text))

    title = yams.pop('title')
    date = datetime.strptime(yams.pop('date'), '%Y/%m/%d %H:%M:%S').date()
    tags = yams.pop('categories', '').lower()

    fields = [
        ('Date', date.strftime('%d %B %Y').lstrip('0')),
        ]
    if tags:
        fields.append(('Tags', tags))

    info = {
        'add_disqus': yams.pop('add_disqus', False),
        'add_mathjax': yams.pop('add_mathjax', False),
        'date': date,
        'tags': [s.strip().replace(' ', '-') for s in tags.split(',')]
        }

    del yams['permalink']
    if yams:
        print('Unrecognized YAML fields:')
        for name in sorted(yams):
            print(name, yams[name])
        exit(2)

    rule = '=' * len(title)
    lines = ['', rule, title, rule, '', '']
    lines.extend(':{}: {}'.format(name, value) for name, value in fields)
    return '\n'.join(lines), info, body


def main():
    builder = Builder(magic.compute)
    fs = magic.Filesystem()
    fs._builder = builder

    source_directory = 'texts'
    output_directory = 'output'
    sources = []
    for dirpath, dirnames, filenames in os.walk(source_directory):
        if '.ipynb_checkpoints' in dirnames:
            dirnames.remove('.ipynb_checkpoints')
        for filename in filenames:
            if '.' not in filename:
                continue
            base, ext = filename.rsplit('.', 1)
            if ext not in ('html', 'ipynb', 'rst'):
                continue
            sources.append(os.path.join(dirpath, filename))

    static_directory = 'static'
    statics = []
    for dirpath, dirnames, filenames in os.walk(static_directory):
        if '.ipynb_checkpoints' in dirnames:
            dirnames.remove('.ipynb_checkpoints')
        for filename in filenames:
            statics.append(os.path.join(dirpath, filename))

    blog = Blog(builder, fs)

    documents = []
    for source_path in sources:
        # if 'trivia' not in source_path and 'payroll' not in source_path:
        #     continue
        dirname, filename = os.path.split(source_path)
        dirname = dirname.replace(source_directory, output_directory)
        base, ext = filename.rsplit('.', 1)
        if base == 'index':
            output_path = os.path.join(dirname, 'index.html')
        else:
            output_path = os.path.join(dirname, base, 'index.html')
        post = Document(builder, fs, blog, source_path, output_path)
        documents.append(post)

    blog.documents = documents
    blog.statics = statics

    for document in documents:
        document.parse()
        document.render()

    blog.render_feeds()
    blog.copy_statics()

    with open('test.dot', 'w') as f:
        #pprint(builder.graph._targets)
        f.write(builder.graph.as_graphviz())

    if len(sys.argv) == 1:
        return

    while True:
        fs._wait()
        builder.rebuild()

    return

    import time
    while True:
        print('-')
        time.sleep(1.0)
        for post in posts:
            post._load()
        builder.rebuild()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Exiting')
