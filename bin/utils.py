import re
import yaml
from datetime import datetime
from html.parser import HTMLParser
from io import StringIO
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer

html_parser = HTMLParser()

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

    body_html = re.sub(r'(?s)<pre([^>]*)>(.*?)</pre>', _highlight, html)
    body_html = body_html.replace('\n</pre>', '</pre>')
    return body_html
