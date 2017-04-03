#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from peewee import *

db_location = os.path.join('..', '2-word-segmentation', 'corpus.db')
db = SqliteDatabase(db_location)
db.connect()


class Post(Model):
    user = CharField()
    time = DateTimeField()
    message = TextField(null=True)
    story = CharField(null=True)

    class Meta:
        database = db


class Keyword(Model):
    pid = ForeignKeyField(Post, related_name='keywords')
    rank1 = CharField(null=True)
    rank2 = CharField(null=True)
    rank3 = CharField(null=True)

    class Meta:
        database = db


class Sentiment(Model):
    pid = ForeignKeyField(Post, related_name='sentiments')
    auto_tag = CharField(null=True)
    manual_tag = CharField(null=True)

    class Meta:
        database = db
