#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from urlparse import urljoin

import requests
from bs4 import BeautifulSoup

BASE = 'http://ericlauhuiyik.weebly.com'


def unique(li):
    return list(set(li))


def apply_custom_changes(url, soup):
    script_tag = soup.select('script[src*="slideshow-jq.js"]')
    no_of_script_tag = len(script_tag)
    if no_of_script_tag > 1:
        raise Exception('Expected 1 slideshow-jq.js, got '
                        + str(no_of_script_tag))
    elif no_of_script_tag == 1:
        script_tag[0]['src'] = '/slideshow-jq.js'  # use local version

    # remove weebly sign up banners
    signup_div = soup.find('div', {'id': 'weebly-footer-signup-container'})
    signup_div.extract()

    if url == '/':
        # previously had extra whitespace
        textarea_tag = soup.find('textarea')
        textarea_tag.string = ''

        anchor_tag = soup.select('form .wsite-button')
        del anchor_tag[0]['onclick']
        custom_script = soup.new_tag('script')
        custom_script['src'] = '/formSubmit.js'
        body_tag = soup.find('body')
        body_tag.append(custom_script)

        # make json output readable
        input_tags = soup.find_all('input', {'type': 'text'})
        input_tags[0]['name'] = 'name'
        input_tags[1]['name'] = 'email'
        radio_btns = soup.find_all('input', {'type': 'radio'})
        for btn in radio_btns:
            btn['name'] = 'motive'
        textarea_tag['name'] = 'message'


def apply_custom_output(url, html):
    if url == '/':
        return re.sub(r'>\s+</textarea>', '></textarea>', html)
    return html


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
            'check_for': {'src': True},
            'attr': 'src',
        },
        {
            'tag_name': 'link',
            'check_for': {
                'href': True,
                'rel': 'stylesheet',
            },
            'attr': 'href',
        },
        {
            'tag_name': 'script',
            'check_for': {'src': True},
            'attr': 'src',
        }
    ]
    for asset in static_assets:
        attr = asset['attr']
        tags = soup.find_all(asset['tag_name'], asset['check_for'])
        tags = filter(lambda i: not i[attr].startswith('//'), tags)
        for tag in tags:
            tag[attr] = urljoin(BASE, tag[attr])

    apply_custom_changes(url, soup)
    with open(filename, 'w+') as f:
        html = soup.prettify().encode('utf-8')
        output = apply_custom_output(url, html)
        f.write(output)
        print filename


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
