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
            cm.exception.message
        )
        self.assertEqual(
            400,
            cm.exception.status_code
        )

    def test_status_code_payload(self) :
        message = "some message"
        with self.assertRaises(LudoboxError) as cm:
            raise LudoboxError(message, status_code=403, payload={ "data" : "data"})
        self.assertEqual(
            403,
            cm.exception.status_code
        )
        self.assertEqual(
            { "data" : "data"},
            cm.exception.payload
        )

    def test_error_do_dict(self):
        message = "some message"
        with self.assertRaises(LudoboxError) as cm:
            raise LudoboxError(message)

        print cm.exception.to_dict()
        self.assertEqual(
            { "message" : message},
            cm.exception.to_dict()
        )
