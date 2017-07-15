#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import unittest
from flask_testing import TestCase
from helpers import delete_data_path, create_empty_data_path, add_samples_to_data_dir

from ludobox import create_app
from ludobox.user import get_latest_changes

TEST_DATA_DIR = '/tmp/test-data'

class TestLudoboxUserLogics(TestCase):
    """Functions for user pages and logics"""

    def create_app(self):
        # pass in test configuration
        test_dir = os.path.join(os.getcwd(),"server/tests")
        config_path = os.path.join(test_dir,"config.test.yml")

        # create empy path for data
        delete_data_path(TEST_DATA_DIR)
        create_empty_data_path(TEST_DATA_DIR)

        return create_app(self, config_path=config_path)

    def setUp(self):
        add_samples_to_data_dir(TEST_DATA_DIR)

        # creates a test client
        self.client = self.app.test_client()

        # propagate the exceptions to the test client
        self.client.testing = True

    def test_get_latest_changes(self):

        with self.app.app_context():
            changes = get_latest_changes()
            print changes
            # self.assertFalse(True)
