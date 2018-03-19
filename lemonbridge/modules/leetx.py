# -*- coding: utf-8 -*-

#
# 1337x module
# This is based on the 1337x we-get module:
# https://github.com/rachmadaniHaryono/we-get
#

import re
import util


BASE_URL = "http://1337x.to"
SEARCH_URI = "/search/%s/1/"
MAX_RESULTS = 10


def process_item(link):
    url = "%s%s" % (BASE_URL, link)
    data = util.http_get_request(url)
    links = re.findall(r'href=[\'"]?([^\'">]+)', data)
    seeders = re.findall(r'<span class=\"seeds\">(.*?)</span>', data)[0]
    leechers = re.findall(r'<span class=\"leeches\">(.*?)</span>', data)[0]

    magnet = None
    for link in links:
        if 'magnet' in link:
            magnet = link
            break

    name = None
    name = util.fix_name(util.magnet2name(magnet))

    item = {}
    item.update(
        {name: {'seeds': seeders, 'leeches': leechers, 'link': magnet}}
    )
    return item


def search(search_query):
    url = "%s%s" % (BASE_URL, SEARCH_URI % (search_query))
    data = util.http_get_request(url)
    links = re.findall(r'href=[\'"]?([^\'">]+)', data)

    items = {}
    results = 0
    for i in range(len(links)):
        link = links[i]
        if '/torrent/' in link:
            if results == MAX_RESULTS:
                break
            item = process_item(link)
            items.update(item)
            results += 1
    return items