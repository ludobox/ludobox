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

from ludobox import create_app
from ludobox.run import get_server_port
from ludobox.config import read_config
from ludobox.content import read_content
from ludobox.models import User, Role, db
from ludobox.security import user_datastore

from ludobox.routes.api import rest_api

from helpers import delete_data_path, create_empty_data_path, add_samples_to_data_dir

TEST_DATA_DIR = '/tmp/test-data'

class TestLudoboxWebServer(TestCase):


    def create_app(self):
        # pass in test configuration
        test_dir = os.path.join(os.getcwd(),"server/tests")
        config_path = os.path.join(test_dir,"config.test.yml")

        # create empy path for data
        delete_data_path(TEST_DATA_DIR)
        create_empty_data_path(TEST_DATA_DIR)

        return create_app(self, config_path=config_path)

    def setUp(self):

        self.config = read_config()
        self.app.config['SECRET_KEY'] = 'sekrit!'
        self.app.config["WTF_CSRF_ENABLED"] = False
        self.app.config["LOGIN_DISABLED"] = False

        # create games
        add_samples_to_data_dir(self.app.config["DATA_DIR"])

        # register routes
        self.app.register_blueprint(rest_api)

        # setup db
        db.drop_all()
        db.create_all()

        # create default roles
        user_role = Role(name='contributor')
        super_user_role = Role(name='superuser')
        db.session.add(user_role)
        db.session.add(super_user_role)
        db.session.commit()

        # add a role
        # default_role = user_datastore.find_role("contributor")
        # user_datastore.add_role_to_user(self.user, default_role)
        # db.session.commit()

        # add a user
        self.user_email = "tester@test.com"
        self.user_password = "password"
        rv = self.register(
            email=self.user_email, password=self.user_password
            )

        # creates a test client
        self.client = self.app.test_client()

        # propagate the exceptions to the test client
        self.client.testing = True

    def tearDown(self):
        db.session.remove()

    def register(self, email=None, password=None):
        """Register a user"""
        print email, password
        return self.client.post(
            url_for_security('register'),
            data={
                'email': email,
                'password': password,
                'password_confirm': password
                },
            content_type= 'application/x-www-form-urlencoded',
            follow_redirects=True
        )

    def login(self, email=None, password=None):
        email = email or self.user_email
        password = password or self.user_password
        return self.client.post(
            url_for_security('login'),
            data={'email': email, 'password': password},
            follow_redirects=True
        )

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

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
