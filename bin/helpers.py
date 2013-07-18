"""Routines to help render my web site.

At the moment, these are tasked with doing a great deal of impedance
mismatch between my old blogofile-style blog entries and data, and my
new sleek Make-and-Bottle-powered site generation scripts.  Hopefully
these routines will get less crufty as time goes on and more and more
old content gets migrated!

"""
import os
from datetime import datetime

class Posts(object):
    """My timeline of tagged blog posts."""

    def __init__(self, directory):
        self.posts = []
        filenames = sorted(os.listdir(directory))
        for filename in filenames:
            self.add(os.path.join(directory, filename))

    def add(self, path):
        print path

        with open(path) as f:
            i = stripped_lines(f)
            line = next(i)
            while line != '---':
                line = next(i)
            line = next(i)
            d = {}
            while line != '---':
                key, value = line.split(':', 1)
                d[key.strip()] = value.strip()
                line = next(i)

        if 'draft' in d:
            return

        if 'date' in d:
            d['date'] = datetime.strptime(d['date'], '%Y/%m/%d %H:%M:%S')
        if 'categories' in d:
            d['tags'] = [c.strip().replace(' ', '-')
                         for c in d['categories'].lower().split(',')]

        self.posts.append(d)

    def tags(self):
        t = {}
        for post in self.posts:
            for tag in post['tags']:
                t.setdefault(tag, []).append(post)
        return t


def stripped_lines(fileobj):
    for line in fileobj:
        yield line.strip()
