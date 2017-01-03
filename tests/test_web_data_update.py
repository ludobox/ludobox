#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from ludobox.data.crawler import handshake, build_url
from ludobox.config import read_config

class TestLudoboxWebDataUpdate(unittest.TestCase):
    """Testing utils function"""

    def setUp(self):
        self.config = read_config()

    def test_build_url(self):
        url = build_url("index.json")
        self.assertEquals(url, "http://localhost:8080/api/index.json")

    def test_handshake(self):
        """Should shake hands with the distant server and get its name."""
        base_url = self.config["web_server_url"]
        res = handshake(base_url)
        self.assertEquals(res["name"], "My LudoBox")

    # def test_get_game_index_file(self):
    #     """Should retrieve an index containing all games"""
    #     self.assertTrue(False)
