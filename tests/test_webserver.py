#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import unittest
import shutil

import io
from StringIO import StringIO

from jsonschema import validate, ValidationError

from ludobox.webserver import app, get_server_port
from ludobox.config import read_config
from ludobox.content import read_game_info

class TestLudoboxWebServer(unittest.TestCase):

    def setUp(self):

        self.config = read_config()

        # change data dir
        if os.path.exists('/tmp/data'):
            shutil.rmtree('/tmp/data')
        os.makedirs('/tmp/data')

        app.config["DATA_DIR"] = '/tmp/data'

        # creates a test client
        self.app = app.test_client()

        # propagate the exceptions to the test client
        self.app.testing = True


    def test_get_server_port(self):
        """Test default and custom port for server"""
        self.assertEquals(get_server_port(None), 8080)
        self.assertEquals(get_server_port(4040), 4040)

    def test_home_status_code(self):
        result = self.app.get('/')

        # assert the status code of the response (redirected)
        self.assertEqual(result.status_code, 200)

    def test_handshake_page(self):
        result = self.app.get('/api')

        self.assertEqual(result.status_code, 200)
        # self.assertEqual(json.loads(result.data), {"name" : self.config["ludobox_name"]})

    def test_css(self):
        result = self.app.get('/css/style.css')
        self.assertEqual(result.status_code, 200)

    def test_js(self):
        result = self.app.get('/js/bundle.js')
        self.assertEqual(result.status_code, 200)

    def test_js(self):
        result = self.app.get('/images/favicon.png')
        self.assertEqual(result.status_code, 200)

    def test_schema(self):
        result = self.app.get('/api/schema')
        self.assertEqual(result.status_code, 200)

        schema = json.loads(result.data)
        self.assertIs(type(schema), dict)
        print schema

        self.assertRaises(ValidationError, lambda : validate({ "test" : [1,3,2,4]}, schema))

    def test_files_api_with_no_files(self):
        result = self.app.get('/api/files/dsdqdqs')
        data = json.loads(result.data)
        self.assertEquals(data, [])

    def test_files_api_with_no_files(self):
        result = self.app.get('/api/files/borgia-le-jeu-malsain')
        data = json.loads(result.data)
        self.assertEquals(data, ["README.md"])

    def test_game_index(self):
        result = self.app.get('/api/games')
        data = json.loads(result.data)
        self.assertIs(type(data), list)
        self.assertTrue(type(data[0]), dict)

    def test_upload_allowed(self):
        app.config["UPLOAD_ALLOWED"] = False

        test_app = app.test_client()
        test_app.testing = True

        result = test_app.post('/api/create',
                                data={},
                                content_type='multipart/form-data'
                                )

        self.assertEqual(result.status_code, 401)

    def test_api_add_game(self):

        valid_info = read_game_info(os.path.join(os.getcwd(), 'tests/test-data/test-game'))

        data = {
            'files': [
                (StringIO('my readme'), 'test-README.txt'),
                (StringIO('my rules'), 'test-RULES.txt'),
                (io.BytesIO(b"abcdef"), 'test.jpg')
            ],
            'info': json.dumps(valid_info)
        }

        result = self.app.post('/api/create',
                                data=data,
                                content_type='multipart/form-data'
                                )

        self.assertEqual(result.status_code, 201)
        res = json.loads(result.data)
        self.assertIn("path", res.keys())

        # load JSON info data
        with open(os.path.join(res["path"], 'info.json'), 'r' )as  f:
            stored_info = json.load(f)
        self.assertEqual(stored_info, valid_info)

        # check for files
        written_filenames = os.listdir(os.path.join(res["path"], 'files'))
        self.assertEqual(written_filenames.sort(), [f[1] for f in data["files"]].sort())

    # def test_form_add_game(self):
    #     """Posting data and files using form should create a new game"""
    #
    #     # delete everything first
    #     clean(OUTPUT_DIR)
    #
    #     valid_info = read_game_info(os.path.join(os.getcwd(), 'tests/test-data/test-game'))
    #     data = {
    #         'files': [
    #             (StringIO('my readme'), 'test-README.txt'),
    #             (StringIO('my rules'), 'test-RULES.txt'),
    #             (io.BytesIO(b"abcdef"), 'test.jpg')
    #         ],
    #         'info': json.dumps(valid_info)
    #     }
    #
    #     result = self.app.post('/addgame',
    #                             data=data,
    #                             content_type='multipart/form-data'
    #                             )
    #
    #     # redirect
    #     self.assertEqual(result.status_code, 302)
    #
    #     path = '/tmp/data/borgia-le-jeu-malsain'
    #
    #     # load JSON info data
    #     with open(os.path.join(path, 'info.json'), 'r' )as  f:
    #         stored_info = json.load(f)
    #     self.assertEqual(stored_info, valid_info)
    #
    #     # check for attached files
    #     written_filenames = os.listdir(os.path.join(path, 'files'))
    #     self.assertEqual(written_filenames.sort(), [f[1] for f in data["files"]].sort())
    #
    #     # HTML page created
    #     html_game_path = os.path.join(OUTPUT_DIR, os.path.join("games", 'borgia-le-jeu-malsain'))
    #     print html_game_path
    #     self.assertTrue(os.path.exists(html_game_path))
    #     self.assertTrue(os.path.isdir(html_game_path))
    #     self.assertTrue(os.path.exists(os.path.join(html_game_path, 'index.html')))
