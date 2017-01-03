#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest
import shutil

from ludobox.config import read_config
from ludobox.content import build_index, read_game_info, write_game_info

class TestLudoboxContent(unittest.TestCase):
    """Functions to index, sort and search content"""

    def setUp(self):
        self.config = read_config()
        self.game_path = os.path.join(os.getcwd(), 'tests/test-data/test-game')

    def test_read_game_info(self):
        """Make sure an info file is read properly"""
        info = read_game_info(self.game_path)

    def test_write_game_info_without_attachements(self):
        """Make sure an info file is written properly"""
        # delete existing to prevent error
        shutil.rmtree("/tmp/borgia-le-jeu-malsain")
        info = read_game_info(self.game_path)
        write_game_info(info, None ,'/tmp')

    def test_build_index(self):
        """Should build an index containing all data in this field"""

        build_index()
        self.assertTrue(os.path.exists(self.config["index_path"]))
