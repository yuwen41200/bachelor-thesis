#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from peewee import *

db = SqliteDatabase('corpus.db')
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
    rank1 = CharField()
    rank2 = CharField()
    rank3 = CharField()

    class Meta:
        database = db


class Sentiment(Model):
    pid = ForeignKeyField(Post, related_name='sentiments')
    score = DoubleField()

    class Meta:
        database = db
