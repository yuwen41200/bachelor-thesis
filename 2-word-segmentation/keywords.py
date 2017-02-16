#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import importlib

from snownlp import normal
from snownlp.summary import textrank
# from snownlp.summary import words_merge

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
        print('"stopwords.txt" converted')
        importlib.reload(normal)


def fix_old_data():
    def fixed(string):
        chars = list(string)
        for idx, char in enumerate(chars):
            if char == '，' or char == '。' or char == '？' or char == '！' or char == '；':
                if idx + 1 < len(chars) and chars[idx+1] == ' ':
                    chars[idx+1] = '\t'
        return ''.join(chars)
    for post in Post.select():
        if post.message:
            post.message = fixed(post.message)
            post.save()


def get_keywords():
    normal.stop.update(('http', 'https', '「', '」', '『', '』', '─', '〈', '〉', '會', '請', '不', '都', '更', '最'))
    for post in Post.select():
        if post.message:
            sentences = []
            # message = ''
            for sentence in post.message.split('\t'):
                words = sentence.split(' ')
                words = normal.filter_stop(words)
                sentences.append(words)
                # message += ''.join(words)
            keyword_text_rank = textrank.KeywordTextRank(sentences)
            keyword_text_rank.solve()
            results = []
            for result in keyword_text_rank.top_index(12):
                results.append(result)
            # simple_merge = words_merge.SimpleMerge(message, results)
            # yield post, simple_merge.merge()
            yield post, results


def insert():
    for post, keywords in get_keywords():
        Keyword.create(
            pid=post,
            rank1=keywords[0] if 0 < len(keywords) and keywords[0] else None,
            rank2=keywords[1] if 1 < len(keywords) and keywords[1] else None,
            rank3=keywords[2] if 2 < len(keywords) and keywords[2] else None
        )
        print('"' + str(post.id) + '" inserted')

if __name__ == '__main__':
    # init()
    # fix_old_data()
    insert()
