#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import unittest
import shutil

from jsonschema import ValidationError
from ludobox.config import read_config
from ludobox.content import build_index, read_game_info, write_game_info, validate_game_data

class TestLudoboxContent(unittest.TestCase):
    """Functions to index, sort and search content"""

    def setUp(self):
        self.config = read_config()
        self.game_path = os.path.join(os.getcwd(), 'tests/test-data/test-game')
        self.wrong_game_path = os.path.join(os.getcwd(), 'tests/test-data/wrong-game')

    def test_validate_game_data(self):
        """Make sure an info file is parsed properly"""
        info = read_game_info(self.game_path)
        self.assertEquals(validate_game_data(info), None)

        # make sure error is raised with a basic mistake
        info_wrong = info.copy()
        info_wrong["type"] = 72
        self.assertRaises(ValidationError, lambda:validate_game_data(info_wrong))

    def test_read_game_info(self):
        """Make sure an info file is read properly"""

        info = read_game_info(self.game_path)
        with open(os.path.join(self.game_path, 'info.json'), 'r') as f:
            json_data = json.load(f)

        json_data["slug"] = "2" # add slug

        self.assertEquals(len(info.keys()), len(json_data.keys()) )
        self.assertEquals(sorted(info.keys()), sorted(json_data.keys()))

        # wrong game raises error
        self.assertRaises(ValidationError, lambda:read_game_info(self.wrong_game_path))




    def test_write_game_info_without_attachements(self):
        """Make sure an info file is written properly"""
        # delete existing to prevent error
        tmp_path = "/tmp/borgia-le-jeu-malsain"
        if os.path.exists(tmp_path):
            shutil.rmtree(tmp_path)
        info = read_game_info(self.game_path)
        write_game_info(info, None ,'/tmp')

        # make sure error is raised with a basic mistake
        info_wrong = info.copy()
        info_wrong["type"] = 72
        self.assertRaises(ValidationError, lambda:write_game_info(info_wrong, None ,'/tmp'))


    def test_build_index(self):
        """Should build an index containing all data in this field"""

        build_index()
        self.assertTrue(os.path.exists(self.config["index_path"]))
