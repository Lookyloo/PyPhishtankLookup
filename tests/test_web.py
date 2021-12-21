#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from pyphishtanklookup import PhishtankLookup


class TestBasic(unittest.TestCase):

    def setUp(self):
        self.client = PhishtankLookup(root_url="http://127.0.0.1:5300")

    def test_up(self):
        self.assertTrue(self.client.is_up)
        self.assertTrue(self.client.redis_up())
