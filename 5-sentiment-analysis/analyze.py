#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import datetime

from models import *


def lookup():
    lut_location = os.path.join('..', '1-data-collection', 'dat', 'uid_to_name_map.dat')
    with open(lut_location) as file:
        lut = json.load(file)
    return lut


def fetch_row(post, post_count, neg_post_count):
    if not post.message:
        row_count = 0
        for _ in post.sentiments:
            row_count += 1
        assert row_count == 0
    else:
        row_count = 0
        for sentiment in post.sentiments:
            row_count += 1
            tag = sentiment.manual_tag if sentiment.manual_tag else sentiment.auto_tag
            if tag == 'neg':
                neg_post_count += 1
            else:
                assert tag == 'pos'
            post_count += 1
        assert row_count == 1
    return post_count, neg_post_count


def build():
    lut = lookup()
    print('# Sentiment Analysis')
    # FIRST PART
    print('Name | ', end='')
    sec_line = '--- | '
    start_time = datetime.datetime(2016, 1, 17)
    one_week = datetime.timedelta(7)
    while True:
        end_time = start_time
        start_time = end_time - one_week
        if start_time - one_week < datetime.datetime(2015, 10, 17):
            start_time = datetime.datetime(2015, 10, 17)
        print(str(start_time), 'to', str(end_time), '| ', end='')
        sec_line += '--- | '
        if start_time == datetime.datetime(2015, 10, 17):
            break
    print('Total')
    sec_line += '---'
    print(sec_line)
    # SECOND PART
    for user in Post.select(Post.user).distinct():
        print(lut[user.user], '| ', end='')
        start_time = datetime.datetime(2016, 1, 17)
        one_week = datetime.timedelta(7)
        while True:
            end_time = start_time
            start_time = end_time - one_week
            if start_time - one_week < datetime.datetime(2015, 10, 17):
                start_time = datetime.datetime(2015, 10, 17)
            post_count = 0
            neg_post_count = 0
            for post in Post.select().where((Post.time.between(start_time, end_time)) & (Post.user == user.user)):
                post_count, neg_post_count = fetch_row(post, post_count, neg_post_count)
            print('{:d}/{:d} ({:.2f}%) | '.format(neg_post_count, post_count, neg_post_count/post_count*100), end='')
            if start_time == datetime.datetime(2015, 10, 17):
                break
        post_count = 0
        neg_post_count = 0
        for post in Post.select().where(Post.user == user.user):
            post_count, neg_post_count = fetch_row(post, post_count, neg_post_count)
        print('{:d}/{:d} ({:.2f}%)'.format(neg_post_count, post_count, neg_post_count/post_count*100))

if __name__ == '__main__':
    sys.stdout = open('analyze.md', 'w')
    build()
    sys.stdout = sys.__stdout__
