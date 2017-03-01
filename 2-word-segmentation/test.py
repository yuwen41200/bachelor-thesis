#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from models import *


class CorpusIntegrityTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_post(self):
        for i in range(10):
            with self.subTest(i=i):
                self.assertEqual('foo', str(i))

if __name__ == '__main__':
    unittest.main()
