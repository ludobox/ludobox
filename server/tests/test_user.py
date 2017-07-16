#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json

import unittest
from flask_testing import TestCase
from helpers import delete_data_path, create_empty_data_path, add_samples_to_data_dir

from LudoboxTestCase import LudoboxTestCase
from ludobox import create_app
from ludobox.user import get_latest_changes
from ludobox.routes.api import rest_api

from datetime import datetime
import time

class TestLudoboxUserLogics(LudoboxTestCase):
    """Functions for user pages and logics"""

    def setUp(self):
        pass

    def test_get_latest_changes(self):
        with self.app.app_context():
            changes = get_latest_changes()
            self.assertEqual(len(changes), 2)

            change = changes[0]
            self.assertEqual(change["title"], "Borgia, le jeu malsain")
            self.assertEqual(change["event"]["type"], "create")

    def test_get_latest_changes_for_user(self):
        with self.app.app_context():
            changes = get_latest_changes(user="info@dcalk.org")
            self.assertEqual(len(changes), 1)

            change = changes[0]
            self.assertEqual(change["title"], "Borgia, le jeu malsain")
            self.assertEqual(change["event"]["type"], "create")
            self.assertEqual(change["event"]["user"], "info@dcalk.org")

    def test_get_latest_changes_using_time_limit(self):
        with self.app.app_context():

            # assert we can pass only an *epoch* time
            self.assertRaises(AssertionError, lambda : get_latest_changes(before_time='Jul 9, 2009 @ 20:02:58 UTC'))

            year_2016 = 1451520000 # 31 Dec 2015

            # get changes before 2016
            changes = get_latest_changes(before_time=year_2016)

            # only borgia
            self.assertEqual(len(changes), 1)

    def test_get_latest_changes_filtered_by_time_and_user(self):

        # register API routes
        self.app.register_blueprint(rest_api)

        # load info without history
        valid_info = self.borgia_info_content

        # change title to create a new game
        valid_info["title"] = "Game of trolls"

        data = {
            'info': json.dumps(valid_info)
        }

        with self.client:

            email_dcalk = "info@dcalk.org"
            self.register(email=email_dcalk, password="password")
            self.login(email=email_dcalk)

            # create the game through API
            result = self.client.post('/api/create',
                                    data=data,
                                    content_type='multipart/form-data'
                                    )
            self.assertEqual(result.status_code, 201)

            # make sure changes
            changes = get_latest_changes(user=email_dcalk)
            self.assertEqual(len(changes), 2)

            # get changes before 2016 and user
            year_2016 = 1451520000 # 31 Dec 2015
            changes = get_latest_changes(user=email_dcalk, before_time=year_2016)

            # only borgia
            self.assertEqual(len(changes), 1)
