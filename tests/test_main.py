#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import unittest
from mock import patch

from ludobox.main import config_parser, main

class TestLudoboxMain(unittest.TestCase):
    """Testing the main Ludobox CLI tool"""

    def test_config_parser_serve(self) :
        testargs = ["ludobox", "serve", "--port", "1234", "--debug"]
        with patch.object(sys, 'argv', testargs) :
            parser = config_parser()
            args = parser.parse_args()
            print args
            self.assertTrue(args.debug)
            self.assertEquals(args.port, str(1234))
            self.assertEquals(args.func.__name__, "serve")
