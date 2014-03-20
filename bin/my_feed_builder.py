#!/usr/bin/env python

import datetime  # must be imported at top level to eval() dictionary
import os
import re
import sys
import time
from email.utils import formatdate

import xml.etree.ElementTree as etree
from pytz import timezone

from helpers import truncate_at_more

atom_ns = 'http://www.w3.org/2005/Atom'
content_ns = 'http://purl.org/rss/1.0/modules/content/'
utc = timezone('GMT')
midnight = datetime.time(0, 0, 0)
time_format = '%a, %d %b %Y %H:%M:%S GMT'

def cut_off_h1(body):
    if '<h1' in body:
        body = body.split(u'</h1>')[1]
    if '<table class="docinfo" ' in body:
        body = body.split(u'</table>', 1)[1]
    return body

def make_links_absolute(body):
    body = body.replace('href="/', 'href="http://rhodesmill.org/')
    return body

def render_feed(tag, posts):
    if not posts:
        return b''

    ttag = tag.title()
    sub = etree.SubElement

    etree.register_namespace('atom', atom_ns)
    etree.register_namespace('content', content_ns)

    feed = etree.Element('rss', version='2.0')
    channel = sub(feed, 'channel')
    sub(channel, '{%s}link' % atom_ns, rel="self", type="application/rss+xml",
        href="http://rhodesmill.org/brandon/category/python/feed/")
    sub(channel, 'link').text = "http://rhodesmill.org/brandon/"
    pubDate = sub(channel, 'pubDate')
    sub(channel, 'title').text = "{} posts by Brandon Rhodes".format(ttag)
    sub(channel, 'description').text = "Blog posts about {}".format(ttag)

    items = []  # (date, element) tuples

    for post in posts:
        url = 'http://rhodesmill.org' + post.url_path

        body = post.body_html
        body = cut_off_h1(body)
        body = truncate_at_more(body, url)
        body = make_links_absolute(body)

        item = etree.Element('item')
        sub(item, 'guid').text = url
        sub(item, 'link').text = url
        sub(item, 'title').text = post.title
        sub(item, 'pubDate').text = post.date.strftime(time_format)
        sub(item, '{%s}encoded' % content_ns).text = body

        items.append((post.date, item))

    items.sort(reverse=True, key=lambda item: item[0])
    for date, element in items[:10]:
        channel.append(element)

    most_recent_date = max(post.date for post in posts)
    pubDate.text = most_recent_date.strftime(time_format)

    return etree.tostring(feed)
