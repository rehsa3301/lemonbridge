# -*- coding: utf-8 -*-

import requests

from random import choice


def start_session():
    with open('static/useragents.txt') as f:
        USER_AGENT = choice(f.read().splitlines())
    session = requests.Session()
    session.headers.update({'User-Agent': USER_AGENT})
    return session
