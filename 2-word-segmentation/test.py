#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from unicodedata import category

import dateutil.parser

from segmentation import read
from models import *


class CorpusIntegrityTest(unittest.TestCase):

    def setUp(self):
        self.posts = []
        with open('segmentation.log') as file:
            for line in file:
                assert line[0] == '"' and line[-11:] == '" inserted\n'
                self.posts.append(line[1:-11])

    def tearDown(self):
        remaining_posts = list(filter(lambda x: x != 'TESTED', self.posts))
        assert len(remaining_posts) == 0

    def test_post(self):
        for pid, user, time, message, story in read():
            idx = self.posts.index(pid)
            post = Post.get(Post.id == idx + 1)
            with self.subTest(idx=idx, pid=pid):
                self.assertEqual(user, post.user)
                time = dateutil.parser.parse(time)
                self.assertEqual(time, post.time)
                message = message.replace('\n', '。').replace('\t', '').replace(' ', '')
                message = message.encode(encoding='big5', errors='replace')
                message = message.decode(encoding='big5', errors='replace')
                sanitized_message = ''
                for char in message:
                    sanitized_message += '\ufffd' if category(char).startswith('C') else char
                post_message = post.message.replace('\t', '').replace(' ', '')
                self.assertEqual(sanitized_message, post_message)
                self.assertEqual(story, post.story)
            self.posts[idx] = 'TESTED'

if __name__ == '__main__':
    unittest.main()
