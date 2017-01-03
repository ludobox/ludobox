#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest

from ludobox.config import read_config
from ludobox.content import build_index, read_game_info

class TestLudoboxContent(unittest.TestCase):
    """Functions to index, sort and search content"""

    def setUp(self):
        self.config = read_config()

    def test_read_game_info(arg):
        """Make sure an info file is read properly"""
        path = os.path.join(os.getcwd(), 'tests/test-data/test-game/info.json')
        read_game_info(path)
        self.assertTrue(False)

    def test_build_index(self):
        """Should build an index containing all data in this field"""

        build_index()
        self.assertTrue(os.path.exists(self.config["index_path"]))
