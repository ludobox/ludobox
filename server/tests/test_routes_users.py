#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_security import current_user, url_for_security

from ludobox.routes.api import rest_api
from ludobox.routes.users import users_api

# test helpers
from LudoboxTestCase import LudoboxTestCase
from helpers import delete_data_path, create_empty_data_path, add_samples_to_data_dir

class TestLudoboxUsersServer(LudoboxTestCase):

    def setUp(self):

        # register routes
        self.app.register_blueprint(rest_api)
        self.app.register_blueprint(users_api)

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

    def test_user_profile(self):
        """Check if we get profile for any user properly"""
        with self.client:

            # self.register(email="info@dcalk.org", password="password")
            # self.login(email="info@dcalk.org")

            result = self.client.get('/api/profile/1')
            self.assertEqual(result.status_code, 200)

            profile = result.json
            self.assertEqual(profile["email"], "tester@test.com")
            self.assertEqual(type(profile["recent_changes"]), list)
            self.assertEqual(len(profile["recent_changes"]), 1)

    def test_get_recent_changes(self):
        """Check if we get recent changes"""
        with self.client:

            result = self.client.get('/api/recent_changes')
            self.assertEqual(result.status_code, 200)
            changes = result.json
            self.assertEqual(len(changes), 2)
            self.assertEqual(changes[0]["event"]["type"], "create")

            # filter for a single user
            result = self.client.get('/api/recent_changes?user_id=1')
            self.assertEqual(result.status_code, 200)
            changes = result.json
            self.assertEqual(len(changes), 1)
            self.assertEqual(changes[0]["event"]["type"], "create")

            # filter limit by time
            year_2016 = 1451520000 # 31 Dec 2015
            result = self.client.get('/api/recent_changes?before_time=%s'%year_2016)
            self.assertEqual(result.status_code, 200)
            changes = result.json
            self.assertEqual(len(changes), 1)
            self.assertEqual(changes[0]["event"]["type"], "create")

    # sadly, can not test with current user
    # def test_current_user_profile(self):
    #     """Check if current user get its profile properly"""
    #     with self.client:
    #         self.login()
    #         result = self.client.get('/api/profile')
    #         self.assertEqual(result.status_code, 200)
    #         profile = result.json
    #         self.assertEqual(profile["email"], self.user_email)
    #         self.assertEqual(type(profile["recent_changes"]), list)
    #         self.assertEqual(len(profile["recent_changes"]), 2)
