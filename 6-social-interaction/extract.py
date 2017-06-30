#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import json
import subprocess
import urllib.parse


def build_lookup():
    lookup_path = os.path.join('..', '1-data-collection', 'dat', 'uid_to_name_map.dat')
    with open(lookup_path) as file:
        _lookup = json.load(file)
    return _lookup


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


def inquire_name(query):
    if query in lookup:
        return lookup[query]
    elif query in lookup.values():
        return query
    else:
        print(query + ' => ', end='', flush=True)
        php_script = os.path.join('..', '1-data-collection', 'inquire.php')
        query += '\n'
        try:
            completed_process = subprocess.run(
                ['php', php_script],
                input=query,
                stdout=subprocess.PIPE,
                check=True,
                encoding='utf-8'
            )
        except subprocess.CalledProcessError as called_process_error:
            print('?', flush=True)
            result = called_process_error.stdout
            result = result[result.find('\n')+1:]
            print(result, end='', flush=True)
            result = None
        else:
            result = completed_process.stdout
            result = result[result.find('\n')+1:]
            print(result, end='', flush=True)
            result = result[:-1]
        query = query[:-1]
        lookup[query] = result
        return result


def parse_url(url):
    parse_result = urllib.parse.urlparse(url)
    if 'facebook.com' in parse_result.netloc:
        parts = parse_result.path.split('/')
        if len(parts) >= 2 and not parts[0] and parts[1] and '.php' not in parts[1]:
            return inquire_name(parts[1])
        elif len(parts) >= 1 and parts[0] and '.php' not in parts[0]:
            return inquire_name(parts[0])
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
        dest = lookup[path[8:-5]]
        with open(os.path.join(parent, path)) as file:
            posts = json.load(file)
            for post in posts:
                relations = set()
                if 'message' in post:
                    urls = find_url(post['message'])
                    for url in urls:
                        origin = parse_url(url)
                        if origin and origin != dest:
                            relations.add((dest, origin))
                if 'story' in post:
                    origin = find_origin(post['story'])
                    if origin and origin != dest:
                        relations.add((dest, origin))
                if 'link' in post:
                    origin = parse_url(post['link'])
                    if origin and origin != dest:
                        relations.add((dest, origin))
                for relation in relations:
                    yield relation


def dump_relations():
    with open('extract.csv', 'w') as file:
        for relation in fetch_relation():
            file.write(relation[1] + ';' + relation[0] + '\n')

if __name__ == '__main__':
    lookup = build_lookup()
    dump_relations()
