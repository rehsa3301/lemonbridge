# -*- coding: utf-8 -*-

import requests
import urllib.parse

from html import unescape as html_decode


def http_get_request(url):
    from main import session
    return session.get(url).text


def http_get_request_raw(url):
    from main import session
    return session.get(url)


def magnet2name(link):
    return link.split("&")[1].split("dn=")[1]


def fix_name(name):
    name = html_decode(name)
    return urllib.parse.unquote(
        name.replace('+', '.')
            .replace('[', '')
            .replace(']', '')
            .replace(' ', '.')
            .replace('\'', '')
        )
