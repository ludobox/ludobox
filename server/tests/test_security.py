#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import unittest
import shutil
import time

from flask_testing import TestCase
from flask_security import current_user, url_for_security

from ludobox import create_app
from ludobox.models import User, Role, db, create_default_roles
from ludobox.security import user_datastore

from ludobox.routes.api import rest_api


class TestLudoboxWebServer(TestCase):

    def create_app(self):
        # pass in test configuration
        test_dir = os.path.join(os.getcwd(),"server/tests")
        config_path = os.path.join(test_dir,"config.test.yml")

        return create_app(self, config_path=config_path)

    def setUp(self):

        self.app.config["WTF_CSRF_ENABLED"] = False
        self.app.config["LOGIN_DISABLED"] = False

        self.email = "tester@test.com"
        self.password = "password"

        # register routes
        self.app.register_blueprint(rest_api)

        # setup db
        db.drop_all()
        db.create_all()

        # create default roles
        create_default_roles()

        # creates a test client
        self.client = self.app.test_client()

        # propagate the exceptions to the test client
        self.client.testing = True

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def register(self, email=None, password=None):
        """Helper to register"""
        email = email or self.email
        password = password or self.password

        print "Registering a new user : %s"%email

        client = self.client.post(
            url_for_security('register'),
            data={
                'email': email,
                'password': password,
                'password_confirm': password
                },
            content_type= 'application/x-www-form-urlencoded',
            follow_redirects=True
        )

        print "%s users in the db."%db.session.query(User).count()
        return client


    def test_register_should_have_default_role(self):
        """Register a user needs to be assigned a contributor role by default"""


        self.register()
        user = user_datastore.get_user(self.email)
        self.assertTrue(user.has_role("contributor"))

    def test_register_first_user_should_be_admin(self):
        """Register a user needs to be assigned a contributor role by default"""

        email_admin = "superuser@test.com"
        email_user = "normaluser@test.com"

        rv = self.register(email=email_admin)
        superuser = user_datastore.get_user(email_admin)
        self.assertTrue(superuser.has_role("contributor"))
        self.assertTrue(superuser.has_role("superuser"))

        # second guy should not be admin
        # BUG : cannot test 2 consecutive users...
        # rv = self.register(email=email_user)
        # user = user_datastore.get_user(email_user)
        # # print user
        # self.assertTrue(user.has_role("contributor"))
        # self.assertFalse(user.has_role("superuser"))
