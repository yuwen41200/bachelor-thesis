#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import importlib
import datetime

from snownlp import normal
from snownlp.summary import textrank

from models import *


def init():
    num = Keyword.delete().where(Keyword.id > 128).execute()
    print(str(num) + ' rows removed')
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


def get_keywords():
    normal.stop.update((
        'http', 'https', '「', '」', '『', '』', '─', '〈', '〉', '會', '請', '不', '都',
        '更', '最', '很', '上', '下', '...', '…', '#', '人', '｜', '%', '才', '年', '天',
        '還', '卻', '|', '沒', '喔', '只', '大', '說', '@', '前', '後', '次', '全', '位',
        '來', '去', '※', 'Po', 'news.ltn.com.tw/news/politics/breakingnews', '一', '二', '三',
        'www.hchg.gov.tw/zh-tw/Event/NewsDetail', 'www.facebook.com/NTUlawsocietas/photos/gm',
        '849083545206911', '913106525447555', '1', '2', '3', '&', '再', '已', '時', '.......',
        'www.appledaily.com.tw/realtimenews/article/new', '看', '應', '小', '好', '做', '先'
    ))
    start_time = datetime.datetime(2016, 1, 17)
    one_week = datetime.timedelta(7)
    while True:
        end_time = start_time
        start_time = end_time - one_week
        if start_time - one_week < datetime.datetime(2015, 10, 17):
            start_time = datetime.datetime(2015, 10, 17)
        sentences = []
        for post in Post.select().where(Post.time.between(start_time, end_time)):
            if not post.message:
                continue
            for sentence in post.message.split('\t'):
                words = sentence.split(' ')
                words = normal.filter_stop(words)
                sentences.append(words)
        results = []
        if sentences:
            keyword_text_rank = textrank.KeywordTextRank(sentences)
            keyword_text_rank.solve()
            for result in keyword_text_rank.top_index(15):
                results.append(result)
        yield str(start_time) + ' to ' + str(end_time), results
        if start_time == datetime.datetime(2015, 10, 17):
            break


def insert():
    for period, keywords in get_keywords():
        Keyword.create(
            subject=period,
            rank0=keywords[0] if 0 < len(keywords) and keywords[0] else None,
            rank1=keywords[1] if 1 < len(keywords) and keywords[1] else None,
            rank2=keywords[2] if 2 < len(keywords) and keywords[2] else None,
            rank3=keywords[3] if 3 < len(keywords) and keywords[3] else None,
            rank4=keywords[4] if 4 < len(keywords) and keywords[4] else None,
            rank5=keywords[5] if 5 < len(keywords) and keywords[5] else None,
            rank6=keywords[6] if 6 < len(keywords) and keywords[6] else None,
            rank7=keywords[7] if 7 < len(keywords) and keywords[7] else None,
            rank8=keywords[8] if 8 < len(keywords) and keywords[8] else None,
            rank9=keywords[9] if 9 < len(keywords) and keywords[9] else None
        )
        print('"' + period + '" inserted')

if __name__ == '__main__':
    init()
    insert()
