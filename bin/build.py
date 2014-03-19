"""Build process powered by `contingent`."""

import os
#import parse_utils
import re
import sys
from blog_project import Base, compute
from bottle import SimpleTemplate
from builderlib import Builder
from datetime import datetime
from docutils.core import publish_parts
from glob import glob
from html.parser import HTMLParser
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
        source = self.source
        is_blogofile = detect_blogofile(source)
        if is_blogofile:
            source = convert_blogofile(source)

        field_matches = re.findall(r'\n:([^:]+): +(.*)', source)
        fields = {name.lower(): value for name, value in field_matches}

        self.date = datetime.strptime(fields['date'], '%d %B %Y').date()
        self.tags = ['-'.join(phrase.strip().lower().split())
                     for phrase in fields['tags'].split(',')]

        parts = publish_parts(source, writer_name='html',
                              settings_overrides={'initial_header_level': 2})
        body_html = parts['docinfo'] + parts['fragment']
        body_html = pygmentize_pre_blocks(body_html)
        body_html = body_html.replace('\n</pre>', '</pre>')

        self.add_disqus = is_blogofile
        self.add_mathjax = False
        self.body_html = body_html
        self.next_link = None
        self.previous_link = None
        self.title = parts['title']

    def render(self):
        self.parse()
        self.report('rendering')
        template = SimpleTemplate(name='layout.html', lookup=['templates'])
        html = template.render(self.__dict__)
        with open(self.output_path, 'w', encoding='utf-8') as f:
            f.write(html)


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

    empty_string, yaml, body = source.split('---', 2)
    yaml_lines = yaml.strip().splitlines()
    fields = dict(line.strip().split(': ', 1) for line in yaml_lines)

    title = fields.pop('title')
    date = datetime.strptime(fields.pop('date'), '%Y/%m/%d %H:%M:%S').date()
    datestr = date.strftime('%d %B %Y').replace(' 0', ' ')
    tags = fields.pop('categories').lower()
    del fields['permalink']

    if fields:
        print('Unrecognized YAML fields:')
        for name in sorted(fields):
            print(name, fields[name])
        exit(2)

    rule = '=' * len(title)
    lines = ['', rule, title, rule, '', '']
    lines.append(':Date: {}'.format(datestr))
    lines.append(':Tags: {}'.format(tags))
    lines.append(body)
    return '\n'.join(lines)


def main():
    builder = Builder(compute)
    source_directory = 'texts/brandon/2013'
    output_directory = 'output/brandon/2013'

    sources = glob(source_directory + '/*.rst')

    posts = []
    for source_path in sources:
        output_path = (source_path.replace(source_directory, output_directory)
                       .replace('.rst', '/index.html'))
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
