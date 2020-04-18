#!/usr/bin/env python3
#
# Figure out which of my talks might be missing from PyVideo.

import json
import re
import os
from dataclasses import dataclass

def main():
    path = os.path.dirname(__file__) + '/../texts/brandon/talks.html'
    with open(path) as f:
        content = f.read()
    separator = '<div class="talk">\n'
    heading, *talk_texts = content.split(separator)
    pyvideo_talks = list(load_pyvideo_data())
    pyvideo_dict = {talk.title: talk for talk in pyvideo_talks}
    pyvideo_dict.update({
        url: talk for talk in pyvideo_talks for url in talk.video_urls
    })
    talk_texts = [transform(talk_text, pyvideo_dict)
                  for talk_text in talk_texts]
    content = separator.join([heading, separator.join(talk_texts)])
    with open(path + '_new', 'w') as f:
        f.write(content)
    return

@dataclass
class Talk:
    title: str
    video_urls: list

def load_pyvideo_data():
    pyvideo_data = os.path.expanduser('~/pyvideo-data/')
    for dirpath, dirnames, filenames in os.walk(pyvideo_data):
        dirnames.sort()
        for filename in sorted(filenames):
            if filename == 'category.json':
                with open(dirpath + '/' + filename) as f:
                    content = f.read()
                j = json.loads(content)
                conference_title = j['title']
                conference_slug = slugify(conference_title)
                continue
            if not filename.endswith('.json'):
                continue
            with open(dirpath + '/' + filename) as f:
                content = f.read()
            if 'Brandon' not in content or 'Rhodes' not in content:
                continue
            j = json.loads(content)
            title = j['title']
            title_slug = j.get('slug') or slugify(title)
            pyvideo_native_url = 'https://pyvideo.org/{}/{}.html'.format(
                conference_slug,
                title_slug,
            )
            video_urls = [jj['url'] for jj in j['videos']]
            video_urls.append(pyvideo_native_url)
            video_urls = [normalize(url) for url in video_urls]
            yield Talk(
                title=title,
                video_urls=video_urls,
            )

def normalize(url):
    if '//youtu.be/' in url:
        return 'https://www.youtube.com/watch?v=' + url.split('/')[-1]
    return url

LINK = r'<a href="([^"]*)"[\n ]*>([^<]*)</a>'
LINK_PATTERN = re.compile(LINK)
LINKS_PATTERN = re.compile(
    '(' + LINK + '[\n •]*)*' + LINK,
    re.DOTALL,
)

def transform(talk_text, pyvideo_dict):
    # Take entry apart.

    title = re.search(r'<h2>([^<]*)</h2>', talk_text)[1]
    title = title.replace('Keynote: ', '')
    #print(title)
    m = LINKS_PATTERN.search(talk_text)
    links = LINK_PATTERN.findall(m[0])

    # Upgrade links to HTTPS where appropriate.

    links = [(upgrade(url), text) for url, text in links]
    urls_already = set(url for url, text in links)

    # Compare it to PyVideo.

    #print('https://www.youtube.com/watch?v=_SBwUTx6Y7U' in pyvideo_dict)
    for url, text in links:
        talk = pyvideo_dict.get(url)
        if talk is not None:
            break
    else:
        talk = pyvideo_dict.get(title)

    if talk is None:
        print('Not found:', title)
    else:
        for url in talk.video_urls:
            if url in urls_already:
                continue
            if 'pyvideo.org' in url:
                text = 'PyVideo'
            elif 'archive.org/' in url:
                text = 'Archive.org'
            elif '//www.youtube.com/' in url:
                text = 'YouTube'
            else:
                print(url)
                continue
            i = len(links)

            if links[-1][1] == 'slides':
                i -= 1
            links.insert(i, (url, text))

    # Put entry back together.

    link_texts = [
        '<a href="{}">{}</a>'.format(url, text) for url, text in links
    ]
    talk_text = ''.join((
        talk_text[:m.start()],
        '\n    •\n    '.join(link_texts),
        talk_text[m.end():],
    ))
    return talk_text

def upgrade(url):
    if url.startswith('http:'):
        upgradable = (
            'http://i.ytimg.com/',
            'http://pyvideo.org/',
            'http://rhodesmill.org/',
            'http://vimeo.com/',
            'http://www.youtube.com/',
        )
        if url.startswith(upgradable):
            return url.replace('http:', 'https:', 1)
    return url

def old_main_1():
    dn = os.path.dirname
    path = dn(__file__) + '/../texts/brandon/talks.html'
    with open(path) as f:
        lines = list(f)
    my_urls = {}  # url -> title
    for line in lines:
        titles = re.findall('<h2>([^<]*)</h2>', line)
        if titles:
            title = titles[0]
            continue
        urls = re.findall('https[^"]*www.youtube.com[^"]*', line)
        if not urls:
            urls = re.findall('https[^"]*archive.org[^"]*', line)
        if urls:
            url = urls[0]
            my_urls[url] = title

    pyvideo_urls = {}
    pyvideo_native_urls = {}

    pyvideo_data = os.path.expanduser('~/pyvideo-data/')
    for dirpath, dirnames, filenames in os.walk(pyvideo_data):
        dirnames.sort()
        for filename in sorted(filenames):
            if filename == 'category.json':
                with open(dirpath + '/' + filename) as f:
                    content = f.read()
                j = json.loads(content)
                conference_title = j['title']
                conference_slug = slugify(conference_title)
            if not filename.endswith('.json'):
                continue
            with open(dirpath + '/' + filename) as f:
                content = f.read()
            if 'Brandon' not in content or 'Rhodes' not in content:
                continue
            j = json.loads(content)
            title = j['title']
            title_slug = slugify(title)
            url = j['videos'][0]['url']
            pyvideo_urls[url] = title
            pyvideo_native_urls[url] = 'https://pyvideo.org/{}/{}.html'.format(
                conference_slug,
                title_slug,
            )

            # ok = '  OK   ' if expected_url in urls else 'MISSING'
            # print(ok, '-', expected_url)

    all_urls = set(pyvideo_urls)
    all_urls.update(my_urls)

    print('\nBOTH\n')

    both = set(pyvideo_urls) & set(my_urls)
    titles = {my_urls[url] for url in both}
    print('\n'.join(sorted(titles)))

    print('\nMINE\n')

    mine = set(my_urls) - set(pyvideo_urls)
    titles = {my_urls[url] for url in mine}
    print('\n'.join(sorted(titles)))

    print('\nTHEIRS\n')

    theirs = set(pyvideo_urls) - set(my_urls)
    print(theirs)
    titles = {pyvideo_urls[url] for url in theirs}
    reverse = {a: b for b, a in pyvideo_urls.items()}
    for title in sorted(titles):
        print(title)
        external_video_url = reverse[title]
        if 'youtube' in external_video_url:
            name = 'YouTube'
        elif 'archive.org' in external_video_url:
            name = 'Archive.org'
        print(FMT.format(external_video_url, name,
                         pyvideo_native_urls[reverse[title]]))

FMT = """\
    <a href="{}">{}</a>
    •
    <a href="{}">PyVideo</a>
    •"""

# https://pyvideo.org/pycon-ie-2017/you-look-at-it-till-a-solution-occurs.html
# https://pyvideo.org/pycon-ie-2017/you-look-at-it-till-a-solution-occurs.html

def old_main_2():
    dn = os.path.dirname
    path = dn(__file__) + '/../texts/brandon/talks.html'
    with open(path) as f:
        content = f.read()
    urls = re.findall('https[^"]*pyvideo[^"]*', content)

    pyvideo_data = os.path.expanduser('~/pyvideo-data/')
    for dirpath, dirnames, filenames in os.walk(pyvideo_data):
        dirnames.sort()
        for filename in sorted(filenames):
            if filename == 'category.json':
                with open(dirpath + '/' + filename) as f:
                    content = f.read()
                j = json.loads(content)
                conference_title = j['title']
                conference_slug = slugify(conference_title)
            if not filename.endswith('.json'):
                continue
            with open(dirpath + '/' + filename) as f:
                content = f.read()
            if 'Brandon' not in content or 'Rhodes' not in content:
                continue
            # if 'podes' not in content:
            #     continue
            j = json.loads(content)
            title = j['title']
            title_slug = slugify(title)
            expected_url = 'https://pyvideo.org/{}/{}.html'.format(
                conference_slug,
                title_slug,
            )
            ok = '  OK   ' if expected_url in urls else 'MISSING'
            print(ok, '-', expected_url)

def slugify(s):
    s = ''.join(c for c in s if c.isalnum() or c == ' ')
    s = s.lower().replace(' ', '-')[:48]
    s = re.sub(r'-+', '-', s)
    return s

if __name__ == '__main__':
    main()
