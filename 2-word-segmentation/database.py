#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os

import dateutil.parser

from models import *


def read():
    parent = os.path.join('..', '1-data-collection', 'json')
    paths = os.listdir(parent)
    for path in paths:
        with open(os.path.join(parent, path)) as file:
            posts = json.load(file)
            for post in posts:
                fields = set(post.keys())
                if (
                    fields == {'id', 'created_time', 'message'}
                    or fields == {'id', 'created_time', 'message', 'story'}
                    or fields == {'id', 'created_time', 'story'}
                ):
                    pid = post['id']
                    user = path[8:-5]
                    time = post['created_time']
                    message = post['message'] if 'message' in post else None
                    story = post['story'] if 'story' in post else None
                    yield pid, user, time, message, story
                else:
                    print('corrupted data in {}'.format(path))
                    for key, value in post.items():
                        print(key, ': ', value)


def segment(message):
    pass
    return 'return segmentation of ' + message


def insert():
    db.create_tables([Post, Keyword, Sentiment], safe=True)
    for pid, user, time, message, story in read():
        time = dateutil.parser.parse(time)
        message = segment(message) if message else None
        Post.create(user=user, time=time, message=message, story=story)
        print('"' + pid + '" inserted')

if __name__ == '__main__':
    db.drop_tables([Post, Keyword, Sentiment], safe=True)
    insert()
