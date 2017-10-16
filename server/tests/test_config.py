#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest
import shutil

from ludobox.config import read_config, validate_config

TEST_DATA_DIR = '/tmp/test-data'

class TestLudoboxConfig(unittest.TestCase):
    """Testing the load/write config for the Ludobox"""

    def setUp(self):
        """Init the tests"""

        data_dir = os.path.join(os.getcwd(),"data")
        index_path = os.path.join(data_dir, 'index.json')

        if os.path.exists(TEST_DATA_DIR):
            shutil.rmtree(TEST_DATA_DIR)
        os.makedirs(TEST_DATA_DIR)

        self.default_values = {
            "web_server_url" : None,
            "port" : 8080,
            "data_dir" : data_dir,
            "index_path" :index_path,
            "ludobox_name" : "My LudoBox",
            "upload_allowed" : True,
            "database_uri" : "sqlite:////tmp/ludobox.db",
            "max_file_size" : 20
        }

    def test_read_config_default(self):
        """Default config should have correct values"""

        config = read_config()

        # make sure keys are the same
        self.assertEquals(len(config.keys()), len(self.default_values.keys()) )
        print config.keys()
        self.assertEquals(sorted(config.keys()), sorted(self.default_values.keys()))
        self.assertEquals(config, self.default_values)

    def test_read_config_custom_values(self):
        """Config should parse value from the config file"""
        test_config_file = os.path.join(os.getcwd(),"server/tests/config.test.yml")
        config = read_config(config_path=test_config_file)

        self.assertEquals(config["port"], 4000)
        self.assertEquals(config["ludobox_name"], "My Testing LudoBox")
        self.assertEquals(config["web_server_url"], "http://localhost:8080")
        self.assertEquals(config["database_uri"], "sqlite:////tmp/test-for-testing.db")

        # tests file and dir paths
        self.assertEquals(config["data_dir"], '/tmp/test-data')

    def test_read_config_wrong_values(self):
        """Config should identify wrong values"""

        config = self.default_values.copy()
        config["port"] = "5000"
        self.assertRaises(AssertionError, lambda: validate_config(config))

        config = self.default_values.copy()
        config["ludobox_name"] = 12
        self.assertRaises(AssertionError, lambda:validate_config(config))

        config = self.default_values.copy()
        config["web_server_url"] = "ludobox"
        self.assertRaises(AssertionError, lambda:validate_config(config))

        # validate data path
        config = self.default_values.copy()
        config["data_dir"] = "/home/ludobox"
        self.assertRaises(ValueError, lambda:validate_config(config))

        # make sure that there is an URL in
        config = self.default_values.copy()
        config["web_server_url"] = ""
        self.assertRaises(AssertionError, lambda:validate_config(config))
        config["web_server_url"] = None
        validate_config(config)
