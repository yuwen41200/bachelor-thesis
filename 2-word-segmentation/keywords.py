#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import importlib

from snownlp import normal
from snownlp.summary import textrank
from snownlp.summary import words_merge

from models import *


def init():
    Keyword.drop_table(fail_silently=True)
    Keyword.create_table(fail_silently=True)
    if not os.path.isfile(normal.stop_path + '.zhtw'):
        subprocess.run([
            'opencc',
            '-i', normal.stop_path,
            '-o', normal.stop_path + '.zhtw',
            '-c', 's2twp.json'
        ], check=True)
        subprocess.run(['cp', normal.stop_path + '.zhtw', normal.stop_path], check=True)
        importlib.reload(normal)


def get_keywords():
    for post in Post.select():
        if post.message:
            words = post.message.split(' ')
            message = ''.join(words)
            words = normal.filter_stop(words)
            keyword_text_rank = textrank.KeywordTextRank(words)
            keyword_text_rank.solve()
            results = []
            for result in keyword_text_rank.top_index(10):
                results.append(result)
            simple_merge = words_merge.SimpleMerge(message, results)
            yield post, simple_merge.merge()


def insert():
    for post, keywords in get_keywords():
        Keyword.create(
            pid=post,
            rank1=keywords[0] or None,
            rank2=keywords[1] or None,
            rank3=keywords[2] or None
        )
        print('"' + post.id + '" inserted')

if __name__ == '__main__':
    # init()
    insert()
