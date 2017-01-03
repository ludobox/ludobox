#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from ludobox.utils import validate_url

class TestLudoboxUtils(unittest.TestCase):
    """Testing utils function"""

    def test_validate_url(self):
        """Should detect wrong URLs"""
        self.assertTrue(validate_url("http://google.com") )
        self.assertTrue(validate_url("http://localhost:3000") )
        self.assertTrue(validate_url("https://localhost:3000") )
        self.assertTrue(validate_url("https://box.ludobox.net") )
        self.assertTrue(not validate_url("lalal") )
        self.assertTrue(not validate_url("guzzt") )
