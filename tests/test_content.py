#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import unittest
import shutil

import io
from StringIO import StringIO

from jsonschema import ValidationError

from ludobox.config import read_config
from ludobox.content import build_index, read_game_info, validate_game_data, allowed_file, clean_game
from ludobox.content import write_game, write_info_json, write_attachments


class TestLudoboxContent(unittest.TestCase):
    """Functions to index, sort and search content"""

    def setUp(self):
        self.config = read_config()
        self.game_path = os.path.join(os.getcwd(), 'tests/test-data/test-game')
        self.wrong_game_path = os.path.join(os.getcwd(), 'tests/test-data/wrong-game')

        self.tmp_path = "/tmp/test-le-jeu-coquin"
        clean_game(self.tmp_path)

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

    def test_allowed_files(self):
        """Check if filenames are allowed"""

        self.assertTrue(allowed_file("bla.txt"))
        self.assertTrue(allowed_file("bla.png"))
        self.assertTrue(allowed_file("bla.jpg"))
        self.assertTrue(allowed_file("bla.gif"))
        self.assertTrue(allowed_file("bla.stl"))
        self.assertTrue(allowed_file("bla.zip"))
        self.assertFalse(allowed_file("bla.xxx"))
        self.assertFalse(allowed_file("bla.123"))

    def test_writing_invalid_data(self):
        """Make sure an error is raised before writing invalid data"""
        info = read_game_info(self.game_path)
        info_wrong = info.copy()
        info_wrong["type"] = 72
        self.assertRaises(ValidationError, lambda:write_info_json(info_wrong, self.tmp_path))

    def test_clean_game(self):
        """Make sure the directory is erased properly"""
        os.makedirs(self.tmp_path) # create game path
        clean_game(self.tmp_path)
        self.assertFalse(os.path.exists(self.tmp_path))

    def test_write_info_json(self):
        """Make sure the JSON info file is written properly"""

        # load data
        info = read_game_info(self.game_path)

        # create game path and write info file
        os.makedirs(self.tmp_path)
        write_info_json(info, self.tmp_path)

        # check if data has been written correctly
        info_path = os.path.join(self.tmp_path, 'info.json')
        self.assertTrue(os.path.exists(info_path))
        with open(info_path, "r") as f :
            data = json.load(f)
        self.assertEquals(info, data)

    # TODO : find a way to test without Flask (tested in test_webserver.py anyway)
    # def test_write_attachments(self):
    #     """Make sure attachments are saved properly"""
    #
    #     test_files = [
    #         (StringIO('my readme'), 'test-README.txt'),
    #         (StringIO('my rules'), 'test-RULES.txt'),
    #         (io.BytesIO(b"abcdef"), 'test.jpg')
    #     ]
    #
    #     # create game path
    #     os.makedirs(self.tmp_path)
    #
    #     write_attachements(test_files, self.tmp_path)


    def test_build_index(self):
        """Should build an index containing all data in this field"""

        build_index()
        self.assertTrue(os.path.exists(self.config["index_path"]))
