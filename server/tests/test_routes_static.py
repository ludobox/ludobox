#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json

from flask_testing import TestCase

from jsonschema import validate, ValidationError

from ludobox import create_app
from ludobox.routes.static import statics

class TestLudoboxWebServerStatic(TestCase):

    def setUp(self):
        self.app.register_blueprint(statics)
        self.client = self.app.test_client()

    def create_app(self):
        # pass in test configuration
        test_dir = os.path.join(os.getcwd(),"server/tests")
        config_path = os.path.join(test_dir,"config.test.yml")
        return create_app(self, config_path=config_path)

    def test_css(self):
        result = self.client.get('/css/style.css')
        self.assertEqual(result.status_code, 200)

    # def test_js(self):
    #     result = self.client.get('/js/bundle.js')
    #     self.assertEqual(result.status_code, 200)

    def test_images(self):
        result = self.client.get('/images/favicon.png')
        self.assertEqual(result.status_code, 200)

    def test_game_schema(self):
        result = self.client.get('/api/schema/game')
        self.assertEqual(result.status_code, 200)

        schema = json.loads(result.data)
        self.assertIs(type(schema), dict)

        self.assertRaises(ValidationError, lambda : validate({ "test" : [1,3,2,4]}, schema))
