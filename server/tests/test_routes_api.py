#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import unittest
import shutil

import io
from StringIO import StringIO

from flask_testing import TestCase

from jsonschema import validate, ValidationError

from flask import session
from flask_security import current_user, url_for_security

from ludobox.run import get_server_port
from ludobox.content import read_content
from ludobox.models import User, Role, db
from ludobox.security import user_datastore

from ludobox.routes.api import rest_api

# test helpers
from LudoboxTestCase import LudoboxTestCase
from helpers import delete_data_path, create_empty_data_path, add_samples_to_data_dir

TEST_DATA_DIR = '/tmp/test-data'

class TestLudoboxWebServer(LudoboxTestCase):

    def setUp(self):

        # register routes
        self.app.register_blueprint(rest_api)

        # register a new user
        rv = self.register(
            email=self.user_email,
            password=self.user_password
            )

    def test_login_logout(self):
        rv = self.login(email=None, password=None)
        self.assertFalse(current_user.is_authenticated)
        rv = self.logout()
        self.assertFalse(current_user.is_authenticated)
        with self.client:
            self.login()
            self.assertTrue(current_user.is_authenticated)

    def test_get_server_port(self):
        """Test default and custom port for server"""
        self.assertEquals(get_server_port(None), 8080)
        self.assertEquals(get_server_port(4040), 4040)

    def test_home_status_code(self):
        result = self.client.get('/')

        # assert the status code of the response (redirected)
        self.assertEqual(result.status_code, 200)

    def test_handshake_page(self):
        result = self.client.get('/api')

        self.assertEqual(result.status_code, 200)
        # self.assertEqual(json.loads(result.data), {"name" : self.config["ludobox_name"]})

    def test_files_api_with_no_files(self):
        result = self.client.get('/api/files/dsdqdqs')
        data = json.loads(result.data)
        self.assertEquals(data, [])

    def test_files_api_with_no_files(self):
        result = self.client.get('/api/files/borgia-le-jeu-malsain-fr')
        data = json.loads(result.data)
        self.assertEquals(data, ["README.md"])

    def test_game_index(self):
        result = self.client.get('/api/games')
        data = json.loads(result.data)
        self.assertIs(type(data), list)
        self.assertTrue(type(data[0]), dict)

    def test_upload_allowed(self):
        # self.login(email=self.user_email, password=self.user_password)
        self.app.config["UPLOAD_ALLOWED"] = False

        with self.client:
            self.login()
            result = self.client.post('/api/create',
                                    data={},
                                    content_type='multipart/form-data'
                                    )

            self.assertEqual(result.status_code, 401)

    def test_add_game_forbidden(self):
        """Make sure only logged in user can add content"""

        valid_info = self.borgia_info_content

        delete_data_path(self.app.config["DATA_DIR"])
        create_empty_data_path(self.app.config["DATA_DIR"])

        data = {
            'files': [
                (StringIO('my readme'), 'test-README.txt'),
                (StringIO('my rules'), 'test-RULES.txt'),
                (io.BytesIO(b"abcdef"), 'test.jpg')
            ],
            'info': json.dumps(valid_info)
        }

        with self.app.test_client() as c:

            print current_user

            result = c.post('/api/create',
                                    data=data,
                                    content_type='multipart/form-data'
                                    )

            print result.data
            self.assertEqual(result.status_code, 403)

    def test_api_create_content(self):

        # create empy path for data
        delete_data_path(TEST_DATA_DIR)
        create_empty_data_path(TEST_DATA_DIR)

        # load info without history
        with open(os.path.join(os.getcwd(), "server/tests/test-data/borgia-no-history.json"), 'r') as f:
            valid_info = json.load(f)

        data = {
            'files': [
                (StringIO('my readme'), 'test-README.txt'),
                (StringIO('my rules'), 'test-RULES.txt'),
                (io.BytesIO(b"abcdef"), 'test.jpg')
            ],
            'info': json.dumps(valid_info)
        }
        with self.client:
            self.login()
            result = self.client.post('/api/create',
                                    data=data,
                                    content_type='multipart/form-data'
                                    )
            print result.data
            self.assertEqual(result.status_code, 201)

            res = json.loads(result.data)
            self.assertIn("path", res.keys())

            # load JSON info data
            with open(os.path.join(res["path"], 'info.json'), 'r' )as  f:
                stored_info = json.load(f)
            self.assertEquals(stored_info["title"], valid_info["title"])

            # check for files
            written_filenames = os.listdir(os.path.join(res["path"], 'files'))
            self.assertEqual(written_filenames.sort(), [f[1] for f in data["files"]].sort())

    # def test_form_add_game(self):
    #     """Posting data and files using form should create a new game"""
    #
    #     # delete everything first
    #     clean(OUTPUT_DIR)
    #
    #     valid_info = read_content(os.path.join(os.getcwd(), 'server/tests/test-data/test-game'))
    #     data = {
    #         'files': [
    #             (StringIO('my readme'), 'test-README.txt'),
    #             (StringIO('my rules'), 'test-RULES.txt'),
    #             (io.BytesIO(b"abcdef"), 'test.jpg')
    #         ],
    #         'info': json.dumps(valid_info)
    #     }
    #
    #     result = self.client.post('/addgame',
    #                             data=data,
    #                             content_type='multipart/form-data'
    #                             )
    #
    #     # redirect
    #     self.assertEqual(result.status_code, 302)
    #
    #     path = '/tmp/data/borgia-le-jeu-malsain-fr'
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
    #     html_game_path = os.path.join(OUTPUT_DIR, os.path.join("games", 'borgia-le-jeu-malsain-fr'))
    #     print html_game_path
    #     self.assertTrue(os.path.exists(html_game_path))
    #     self.assertTrue(os.path.isdir(html_game_path))
    #     self.assertTrue(os.path.exists(os.path.join(html_game_path, 'index.html')))
