#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest

from ludobox.utils import validate_url, get_resource_slug
from ludobox.flat_files import read_info_json

from LudoboxTestCase import LudoboxTestCase

class TestLudoboxUtils(LudoboxTestCase):
    """Testing utils function"""

    def test_validate_url(self):
        """Should detect wrong URLs"""
        self.assertTrue(validate_url("http://google.com") )
        self.assertTrue(validate_url("http://localhost:3000") )
        self.assertTrue(validate_url("https://localhost:3000") )
        self.assertTrue(validate_url("https://box.ludobox.net") )
        self.assertTrue(not validate_url("lalal") )
        self.assertTrue(not validate_url("guzzt") )

    def test_get_resource_slug(self):
        """Make sure the slug contains name of the game + language"""
        borgia_info = self.borgia_info_content
        slug = get_resource_slug(borgia_info)
        self.assertEquals("game-borgia-le-jeu-malsain-fr", slug)
