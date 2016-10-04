#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from peewee import SqliteDatabase

parent = os.path.join('..', '1-data-collection', 'json')
paths = os.listdir(parent)
for path in paths:
    with open(os.path.join(parent, path)) as file:
        posts = json.load(file)
        for post in posts:
            if not 3 <= len(post) <= 4:
                print('error')
            else:
                print(list(post.keys()))
