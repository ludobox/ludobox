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

from flask_security import login_user

from ludobox.app import create_app
from ludobox.run import get_server_port
from ludobox.config import read_config
from ludobox.content import read_content
from ludobox.models import User, db

class TestLudoboxWebServer(TestCase):

    DATA_DIR = '/tmp/data'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/testing.db'
    TESTING = True
    LOGIN_DISABLED = False
    WTF_CSRF_ENABLED = False


    def create_app(self):
        # pass in test configuration
        return create_app(self)

    def setUp(self):

        self.config = read_config()

        # test data
        self.user_email = "tester@test.com"
        self.user_password = "password"

        # change data dir
        if os.path.exists('/tmp/data'):
            shutil.rmtree('/tmp/data')
        os.makedirs('/tmp/data')


        # creates a test client
        # self.client = app.test_client()
        #
        # # propagate the exceptions to the test client
        # self.client.testing = True

        # setup db
        db.create_all()

        # add a user
        user = User(active=True)
        db.session.add(user)
        db.session.commit()

        # login
        check = self.login()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def login(self, email=None, password=None):
        email = email or self.user_email
        password = password or 'password'
        return self.client.post('/login', data={'email': email, 'password': password}, follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.login()
        assert 'You were logged in' in rv.data
        # rv = self.logout()
        # assert 'You were logged out' in rv.data
        # rv = self.login('adminx', 'default')
        # assert 'Invalid username' in rv.data
        # rv = self.login('admin', 'defaultx')
        # assert 'Invalid password' in rv.data

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

    def test_css(self):
        result = self.client.get('/css/style.css')
        self.assertEqual(result.status_code, 200)

    def test_js(self):
        result = self.client.get('/js/bundle.js')
        self.assertEqual(result.status_code, 200)

    def test_images(self):
        result = self.client.get('/images/favicon.png')
        self.assertEqual(result.status_code, 200)

    def test_game_schema(self):
        result = self.client.get('/api/schema/game')
        self.assertEqual(result.status_code, 200)

        schema = json.loads(result.data)
        self.assertIs(type(schema), dict)
        print schema

        self.assertRaises(ValidationError, lambda : validate({ "test" : [1,3,2,4]}, schema))

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
        app.config["UPLOAD_ALLOWED"] = False

        test_app = app.test_client()
        test_app.testing = True

        result = test_app.post('/api/create',
                                data={},
                                content_type='multipart/form-data'
                                )

        self.assertEqual(result.status_code, 401)

    def test_api_add_game(self):

        valid_info = read_content(os.path.join(os.getcwd(), 'server/tests/test-data/test-game'))

        data = {
            'files': [
                (StringIO('my readme'), 'test-README.txt'),
                (StringIO('my rules'), 'test-RULES.txt'),
                (io.BytesIO(b"abcdef"), 'test.jpg')
            ],
            'info': json.dumps(valid_info)
        }

        result = self.client.post('/api/create',
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
