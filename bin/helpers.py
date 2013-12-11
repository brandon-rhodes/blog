"""Routines to help render my web site."""

import datetime

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
        post['rpath'] = '/{}/'.format(
            post['path'].split('/', 1)[1].rsplit('.', 1)[0])
        posts.append(post)
    posts.sort(key=lambda d: d['date'])
    tags = set(tag for post in posts for tag in post['tags'])
    return posts, tags
