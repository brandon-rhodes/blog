"""Routines to help render my web site."""

import datetime

def read_posts():
    global_dict = {'datetime': datetime}
    paths = set()
    for line in open('cache/tags'):
        if line.startswith('#'):
            paths.add(line.strip().split()[2])
    print paths
    posts = []
    for path in paths:
        source = open(path).read()
        post = eval(source, global_dict)
        path = post['path']
        cache_dir, rest = path.split('/', 1)
        assert cache_dir == 'cache'
        relative_name, extension = path.rsplit('.', 1)
        assert extension == 'dict'
        post['permalink'] = 'http://rhodesmill.org/' + relative_name
        posts.append(post)
    posts.sort(key=lambda d: d['date'])
    tags = set(tag for post in posts for tag in post['tags'])
    return posts, tags
