#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import json
import urllib.parse


def find_url(string):
    pattern = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    prog = re.compile(pattern)
    result = prog.findall(string)
    return result


def find_origin(string):
    pattern = ' shared (.*)\'s '
    prog = re.compile(pattern)
    result = prog.search(string)
    if result:
        return result.group(1)
    else:
        return None


def inquire_name():
    pass


def parse_url(url):
    parse_result = urllib.parse.urlparse(url)
    if 'facebook.com' in parse_result.netloc:
        parts = parse_result.path.split('/')
        if len(parts) >= 2 and not parts[0] and parts[1] and '.php' not in parts[1]:
            return parts[1]
        elif len(parts) >= 1 and parts[0] and '.php' not in parts[0]:
            return parts[0]
        else:
            return None
    elif parse_result.netloc:
        return parse_result.netloc
    else:
        return None


def fetch_relation():
    parent = os.path.join('..', '1-data-collection', 'json')
    paths = os.listdir(parent)
    for path in paths:
        dest = path[8:-5]
        with open(os.path.join(parent, path)) as file:
            posts = json.load(file)
            for post in posts:
                if 'message' in post:
                    urls = find_url(post['message'])
                    for url in urls:
                        origin = parse_url(url)
                        if origin:
                            yield dest, origin
                if 'story' in post:
                    origin = find_origin(post['story'])
                    if origin:
                        yield dest, origin
                if 'link' in post:
                    origin = parse_url(post['link'])
                    if origin:
                        yield dest, origin


def dump_relations():
    with open('extract.csv', 'w') as file:
        for relation in fetch_relation():
            file.write(relation[1] + ';' + relation[0] + '\n')

if __name__ == '__main__':
    dump_relations()
