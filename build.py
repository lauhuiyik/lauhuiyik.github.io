#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urlparse import urljoin

import requests
from bs4 import BeautifulSoup

BASE = 'http://ericlauhuiyik.weebly.com'


def unique(li):
    return list(set(li))


def download_page(url, soup=None):
    filename = url[1:]  # /porfolio.html
    if url == '/':
        filename = 'index.html'

    if not soup:
        full_url = urljoin(BASE, url)
        req = requests.get(full_url)
        req.raise_for_status()
        soup = BeautifulSoup(req.text, 'lxml')

    static_assets = [
        {
            'tag_name': 'img',
            'check_for': [
                {'src': True},
            ],
            'attr': 'src',
        },
        {
            'tag_name': 'link',
            'check_for': [
                {'href': True},
                {'rel': 'stylesheet'},
            ],
            'attr': 'href',
        },
        {
            'tag_name': 'script',
            'check_for': [
                {'src': True},
            ],
            'attr': 'src',
        }
    ]
    for asset in static_assets:
        attr = asset['attr']
        tags = soup.find_all(asset['tag_name'], asset['check_for'])
        tags = filter(lambda i: not i[attr].startswith('//'), tags)
        for tag in tags:
            tag[attr] = urljoin(BASE, tag[attr])
    with open(filename, 'w+') as f:
        f.write(soup.prettify().encode('utf-8'))


def download_site():
    """
    Goals: hotlink all the static assets and make sure the relative
    links are set to absolute, download the html files.
    Also, clear the weebly footer.
    """
    req = requests.get(BASE)
    req.raise_for_status()
    html = req.text
    soup = BeautifulSoup(html, 'lxml')
    page_anchors = soup.select('a[href^="/"]')
    page_urls = unique(map(lambda a: a['href'], page_anchors))

    for url in page_urls:
        if url == '/':
            download_page(url, soup)  # reduce work
        else:
            download_page(url)


if __name__ == '__main__':
    download_site()
