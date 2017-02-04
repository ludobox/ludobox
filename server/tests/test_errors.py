#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest

from ludobox.errors import LudoboxError

class TestLudoboxError(unittest.TestCase):
    """Testing the Ludobox errors"""

    def test_message(self) :
        message = "some message"
        with self.assertRaises(LudoboxError) as cm:
            raise LudoboxError(message)
        self.assertEqual(
            message,
            str(cm.exception)
        )
