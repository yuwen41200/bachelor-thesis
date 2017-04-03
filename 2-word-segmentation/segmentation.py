#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from xml.etree import ElementTree
from time import sleep

import dateutil.parser
from ckipclient import CKIPClient

from models import *
from config import *

ckip = CKIPClient(CKIP_IP, CKIP_PORT, CKIP_USERNAME, CKIP_PASSWORD)
ignored_posts = []


def ignore():
    with open('segmentation.log') as file:
        for line in file:
            if line[0] == '"' and line[-11:] == '" inserted\n':
                ignored_posts.append(line[1:-11])
            else:
                print('unknown log message:', line, flush=True)


def read():
    parent = os.path.join('..', '1-data-collection', 'json')
    paths = os.listdir(parent)
    for path in paths:
        with open(os.path.join(parent, path)) as file:
            posts = json.load(file)
            for post in posts:
                fields = set(post.keys())
                # noinspection PyTypeChecker
                if post.get('id', None) in ignored_posts:
                    continue
                elif {'id', 'created_time'} < fields <= {'id', 'created_time', 'message', 'story', 'link'}:
                    pid = post['id']
                    user = path[8:-5]
                    time = post['created_time']
                    message = post['message'] if 'message' in post else None
                    story = post['story'] if 'story' in post else None
                    yield pid, user, time, message, story
                else:
                    print('corrupted data in {}'.format(path), flush=True)
                    for key, value in post.items():
                        print(key + ': ' + value, flush=True)


def segment(message):
    message = message.replace('\n', '。')
    results = ckip.segment(message, pos=False)
    sentences = []
    for sentence in results:
        sentences.append(' '.join(word for word in sentence))
    return '\t'.join(sentences)


def insert():
    db.create_tables([Post, Keyword, Sentiment], safe=True)
    ignore()
    for pid, user, time, message, story in read():
        try:
            time = dateutil.parser.parse(time)
            message = segment(message) if message else None
        except ValueError as err:
            print('ValueError:', err, flush=True)
            print('failed to insert "' + pid + '"', flush=True)
        except OverflowError as err:
            print('OverflowError:', err, flush=True)
            print('failed to insert "' + pid + '"', flush=True)
        except ElementTree.ParseError as err:
            print('ElementTree.ParseError:', err, flush=True)
            print('failed to insert "' + pid + '"', flush=True)
        except ConnectionError as err:
            print('ConnectionError:', err, flush=True)
            print('failed to insert "' + pid + '"', flush=True)
        except OSError as err:
            print('OSError:', err, flush=True)
            print('failed to insert "' + pid + '"', flush=True)
            print('wait 60 seconds...', flush=True)
            sleep(60)
        else:
            Post.create(user=user, time=time, message=message, story=story)
            print('"' + pid + '" inserted', flush=True)

if __name__ == '__main__':
    # db.drop_tables([Post, Keyword, Sentiment], safe=True)
    insert()
