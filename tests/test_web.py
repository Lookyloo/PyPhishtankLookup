#!/usr/bin/env python3

from __future__ import annotations

import unittest

from pyphishtanklookup import PhishtankLookup


class TestBasic(unittest.TestCase):

    def setUp(self) -> None:
        self.client = PhishtankLookup(root_url="http://127.0.0.1:5300")

    def test_up(self) -> None:
        self.assertTrue(self.client.is_up)
        self.assertTrue(self.client.redis_up())
