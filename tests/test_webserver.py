#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import unittest

from ludobox.webserver import app
from ludobox.config import read_config

class TestLudoboxWebServer(unittest.TestCase):

    def setUp(self):

        self.config = read_config()

        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def test_home_status_code(self):
        result = self.app.get('/')

        # assert the status code of the response (redirected)
        self.assertEqual(result.status_code, 302)

    def test_handshake_page(self):
        result = self.app.get('/api')

        self.assertEqual(result.status_code, 200)
        self.assertEqual(json.loads(result.data), {"name" : self.config["ludobox_name"]})
