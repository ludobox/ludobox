#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
from ludobox.main import parse_args

class TestLudoboxMain(unittest.TestCase):
    """Testing the main Ludobox CLI tool"""

    def test_config_parser_serve(self) :
        testargs = ["start", "--port", "1234", "--debug"]
        parser = parse_args(testargs)
        self.assertTrue(parser.debug)
        self.assertEquals(parser.port, str(1234))
        self.assertEquals(parser.func.__name__, "serve")
