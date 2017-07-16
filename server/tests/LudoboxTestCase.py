#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import shutil

import io
from StringIO import StringIO

import unittest
from flask_testing import TestCase
from flask_security import current_user, url_for_security

from helpers import delete_data_path, create_empty_data_path, add_samples_to_data_dir

from ludobox import create_app
from ludobox.config import read_config
from ludobox.models import User, Role, db

TEST_DATA_DIR = '/tmp/test-data'

class LudoboxTestCase(TestCase):
    """Custom test case, including login and all"""

    @classmethod
    def setUpClass(cls):
        """On inherited classes, run our `setUp` method"""
        # Inspired via http://stackoverflow.com/questions/1323455/python-unit-test-with-base-and-sub-class/17696807#17696807
        # source https://gist.github.com/twolfson/13f5f5784f67fd49b245
        if cls is not LudoboxTestCase and cls.tearDown is not LudoboxTestCase.tearDown:
            orig_setUp = cls.tearDown
            def tearDownOverride(self, *args, **kwargs):
                LudoboxTestCase.tearDown(self)
                return orig_tearDown(self, *args, **kwargs)
            cls.tearDown = tearDownOverride

    @classmethod
    def setUpClass(cls):
        """On inherited classes, run our `tearDown` method"""
        if cls is not LudoboxTestCase and cls.setUp is not LudoboxTestCase.setUp:
            orig_setUp = cls.setUp
            def setUpOverride(self, *args, **kwargs):
                LudoboxTestCase.setUp(self)
                return orig_setUp(self, *args, **kwargs)
            cls.setUp = setUpOverride
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
        self.app.config['Debug'] = False
        self.app.config['SECRET_KEY'] = 'sekrit!'
        self.app.config["WTF_CSRF_ENABLED"] = False
        self.app.config["LOGIN_DISABLED"] = False

        self.tmp_path = TEST_DATA_DIR

        # create games
        add_samples_to_data_dir(self.app.config["DATA_DIR"])

        # load info without history
        with open(os.path.join(self.tmp_path, "borgia-no-history.json"), 'r') as f:
            self.borgia_info_content = json.load(f)

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

        # add a user (superuser)
        self.user_email = "tester@test.com"
        self.user_password = "password"

        # creates a test client
        self.client = self.app.test_client()

        # propagate the exceptions to the test client
        self.client.testing = True

        # create random files
        self.files = [
            (StringIO('my readme'), 'test-README.txt'),
            (StringIO('my rules'), 'test-RULES.txt'),
            (io.BytesIO(b"abcdef"), 'test.jpg')
        ]

    def tearDown(self):
        self.logout()
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
