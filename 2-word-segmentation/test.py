#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

import dateutil.parser

from segmentation import read
from models import *


class CorpusIntegrityTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
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
            idx_fix = idx + 1
            # if idx_fix >= 4078:
                # idx_fix += 1
            # if idx_fix >= 5251:
                # idx_fix += 4
            post = Post.get(Post.id == idx_fix)
            with self.subTest(idx=idx_fix, pid=pid):
                self.assertEqual(user, post.user)
                time = dateutil.parser.parse(time)
                post_time = dateutil.parser.parse(post.time)
                self.assertEqual(time, post_time)
                if message:
                    message = message.replace('\n', '。').replace('\u3000', '')
                    message = message.replace('\t', '').replace(' ', '')
                    message = message.encode(encoding='big5', errors='replace')
                    message = message.decode(encoding='big5', errors='replace')
                    post_message = post.message.replace('\t', '').replace(' ', '')
                    self.assertEqual(message, post_message)
                else:
                    self.assertEqual(None, post.message)
                if story:
                    self.assertEqual(story, post.story)
                else:
                    self.assertEqual(None, post.story)
            self.posts[idx] = 'TESTED'


def fix_idx():
    Post.delete().where(Post.id == 4078).execute()
    Post.delete().where(Post.id == 5251).execute()
    Post.delete().where(Post.id == 5252).execute()
    Post.delete().where(Post.id == 5253).execute()
    Post.delete().where(Post.id == 5254).execute()
    Post.update(id=Post.id - 1).where(Post.id >= 4079).where(Post.id <= 5250).execute()
    Post.update(id=Post.id - 5).where(Post.id >= 5255).execute()

if __name__ == '__main__':
    unittest.main()
    # fix_idx()
