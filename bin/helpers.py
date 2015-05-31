# -*- coding: utf-8 -*-
"""Routines to help render my web site."""

import datetime
import re

more_template = '<p><a href="{}">Read the full article...</a></p>'
preview_limit = 256

def truncate_at_more(body, url):
    pieces = re.split(r'<!-- *more *-->', body)
    if len(pieces) == 1:
        return body
    return pieces[0] + more_template.format(url)

def simple_preview(body):
    if '<table class="docinfo"' in body:
        i = body.find('</table>') + len('</table>')
    else:
        i = body.find('</h1>') + len('</h1>')

    preview = ''
    while len(preview) < preview_limit and i < len(body):
        j = body.find('<', i)
        preview += body[i:j]
        i = body.find('>', j) + 1

    j = preview.find(' ', preview_limit)
    if j != -1:
        preview = preview[:j]

    return preview.strip() + u'…'

def read_posts():
    global_dict = {'datetime': datetime}
    paths = set()
    for line in open('cache/tags'):
        if line.startswith('#'):
            paths.add(line.strip().split()[2])
    posts = []
    for path in paths:
        source = open(path).read()
        post = eval(source, global_dict)
        posts.append(post)
    posts.sort(key=lambda d: d['date'])
    tags = set(tag for post in posts for tag in post['tags'])
    return posts, tags

def read_talks(read_text_file):
    body = read_text_file('texts/brandon/talks.html')
    for line in body.splitlines():
        line = line.strip()
        if line.startswith('<a name='):
            target = line.split('"')[1]
            continue
        if line.startswith('<h2>'):
            title = line.split('<h2>')[1].split('</h2>')[0]
            continue
        if line.startswith('20'):
            date = line.split('<')[0].replace(u' ', u'\xa0')
            yield date, target, title
            continue
