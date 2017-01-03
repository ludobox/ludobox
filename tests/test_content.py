#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest

from ludobox.config import read_config
from ludobox.data.content import build_index

class TestLudoboxContent(unittest.TestCase):
    """Functions to index, sort and search content"""

    def setUp(self):
        self.config = read_config()

    def test_build_index(self):
        """Should build an index containing all data in this field"""

        build_index()
        self.assertTrue(os.path.exists(self.config["index_path"]))
