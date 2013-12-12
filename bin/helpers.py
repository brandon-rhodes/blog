"""Routines to help render my web site."""

import datetime
import re

more_template = '<p><a href="{}">Read the full article...</a></p>'

def truncate_at_more(body, url):
    pieces = re.split(r'<!-- *more *-->', body)
    if len(pieces) == 1:
        return body
    return pieces[0] + more_template.format(url)

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
