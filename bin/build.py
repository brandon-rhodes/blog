"""Build process powered by `contingent`."""

import os
import re
import yaml
from blog_project import Base, compute
from bottle import SimpleTemplate
from builderlib import Builder
from datetime import datetime
from docutils.core import publish_parts
from glob import glob
from html.parser import HTMLParser
from io import StringIO
from operator import attrgetter
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter

html_parser = HTMLParser()

class Blog(Base):
    def __init__(self, builder):
        self._builder = builder
        self.posts = []

    def __repr__(self):
        return '<Blog>'

    @property
    def sorted_posts(self):
        print('Re-sorting posts')
        return sorted(self.posts, key=attrgetter('date'))


class Post(Base):

    def __init__(self, builder, source_path, output_path):
        self._builder = builder
        self.source_path = source_path
        self.output_path = output_path
        self._load()

    def __repr__(self):
        return '<Post {!r}>'.format(self.source_path.split('/')[-1])

    def report(self, verb):
        print(verb.title(), self.source_path)

    def _load(self):
        with open(self.source_path, encoding='utf-8') as f:
            self.source = f.read()

    def parse(self):
        self.report('parsing')
        if self.source_path.endswith('.html'):
            self._parse_html()
        elif self.source_path.endswith('.rst'):
            self._parse_rst()

    def _parse_html(self):
        source = self.source
        if detect_blogofile(source):
            heading, flags, other_html = convert_blogofile(source)
            parts = parse_rst(heading)
            body_html = parts['docinfo'] + other_html
            title = html_parser.unescape(parts['title'])
            self.add_disqus = True
        else:
            body_html = source
            h1_list = re.findall(r'<h1>([^<]*)</h1>', body_html)
            title = h1_list[0] if h1_list else 'Untitled'
            self.add_disqus = True

        body_html = pygmentize_pre_blocks(body_html)
        body_html = body_html.replace('\n</pre>', '</pre>')

        self.add_mathjax = False
        self.body_html = body_html
        self.next_link = None
        self.previous_link = None
        self.title = html_parser.unescape(title)

    def _parse_rst(self):
        source = self.source
        if detect_blogofile(source):
            heading, flags, body = convert_blogofile(source)
            source = heading + body
            self.add_disqus = True
            self.add_mathjax = flags['add_mathjax']
        else:
            self.add_disqus = False
            self.add_mathjax = False

        field_matches = re.findall(r'\n:([^:]+): +(.*)', source)
        fields = {name.lower(): value for name, value in field_matches}

        self.date = datetime.strptime(fields['date'], '%d %B %Y').date()
        self.tags = ['-'.join(phrase.strip().lower().split())
                     for phrase in fields['tags'].split(',')]

        parts = parse_rst(source)
        body_html = parts['docinfo'] + parts['fragment']
        body_html = pygmentize_pre_blocks(body_html)
        body_html = body_html.replace('\n</pre>', '</pre>')

        self.body_html = body_html
        self.next_link = None
        self.previous_link = None
        self.title = html_parser.unescape(parts['title'])

    def render(self):
        self.parse()
        self.report('rendering')
        template = SimpleTemplate(name='layout.html', lookup=['templates'])
        html = template.render(self.__dict__)
        with open(self.output_path, 'w', encoding='utf-8') as f:
            f.write(html)


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
    # yaml_lines = yaml.strip().splitlines()
    # yams = dict(line.strip().split(': ', 1) for line in yaml_lines)
    yams = yaml.load(StringIO(yaml_text))

    title = yams.pop('title')
    date = datetime.strptime(yams.pop('date'), '%Y/%m/%d %H:%M:%S').date()
    tags = yams.pop('categories', '').lower()

    fields = [
        ('Date', date.strftime('%d %B %Y').lstrip('0')),
        ]
    if tags:
        fields.append(('Tags', tags))

    flags = {
        'add_disqus': yams.pop('add_disqus', False),
        'add_mathjax': yams.pop('add_mathjax', False),
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
    return '\n'.join(lines), flags, body


def main():
    builder = Builder(compute)
    source_directory = 'texts/brandon'
    output_directory = 'output/brandon'
    sources = (glob(source_directory + '/*/*.html') +
               #glob(source_directory + '/*/*.ipynb') +
               glob(source_directory + '/*/*.rst'))

    posts = []
    for source_path in sources:
        dirname, filename = os.path.split(source_path)
        dirname = dirname.replace(source_directory, output_directory)
        base, ext = filename.rsplit('.', 1)
        if filename == 'index':
            raise RuntimeError('todo')
        else:
            output_path = os.path.join(dirname, base, 'index.html')
        post = Post(builder, source_path, output_path)
        post.render()
        posts.append(post)

    return
    import time
    while True:
        print('-')
        time.sleep(30.0)
        for post in posts:
            post._load()
        builder.rebuild()


if __name__ == '__main__':
    main()
