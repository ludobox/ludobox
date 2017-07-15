#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import unittest
import shutil

import io
from StringIO import StringIO

from jsonschema import ValidationError
from ludobox.errors import LudoboxError

from ludobox.config import read_config

from ludobox.content import get_content_type, validate_content, read_content, create_content, update_content_info, get_content_index, delete_content


class TestLudoboxContent(unittest.TestCase):
    """Functions to index, sort and search content"""

    def setUp(self):
        self.config = read_config()
        self.game_path = os.path.join(os.getcwd(), 'server/tests/test-data/test-game')
        self.wrong_game_path = os.path.join(os.getcwd(), 'server/tests/test-data/wrong-game')

        self.tmp_path = "/tmp/borgia-le-jeu-malsain-en"
        delete_content(self.tmp_path)

    def test_get_content_type(self):
        data = {"content_type" : "game"}
        self.assertEquals(get_content_type(data), "game")

        # raise Error without content_type
        self.assertRaises(LudoboxError, lambda : get_content_type({}))

        data = {"content_type" : "dfsdfsd"}
        self.assertRaises(AssertionError, lambda : get_content_type(data))

        data = {"content_type" : "workshop"}
        self.assertRaises(NotImplementedError, lambda : get_content_type(data))

    def test_borgia_game_data(self):
        """Make sure the borgias are okay with the model"""
        borgia_game_path = os.path.join(os.getcwd(), 'data/borgia-le-jeu-malsain-fr')
        borgia_info = read_content(borgia_game_path)
        self.assertEquals(validate_content(borgia_info), None)

    def test_validate_content(self):
        """Make sure an info file is parsed properly"""
        info = read_content(self.game_path)
        self.assertEquals(validate_content(info), None)

        # make sure error is raised with a basic mistake
        info_wrong = info.copy()
        info_wrong["description"] = 72
        self.assertRaises(ValidationError, lambda:validate_content(info_wrong))

    # TODO test this function with different scenari: existant/inexistant/not readable dir, info.json present/absent/not readable, with/without attached file
    def test_read_content(self):
        """Make sure an info file is read properly"""

        info = read_content(self.game_path)
        self.assertTrue("title" in info.keys())
        self.assertTrue("files" in info.keys())
        self.assertEquals(len(info["files"]),1)
        self.assertEquals(info["slug"], "borgia-le-jeu-malsain-en")

        # Wrong game should raises validation error
        self.assertRaises(ValidationError, lambda:read_content(self.wrong_game_path))

    def test_create_content_without_attachements(self):
        """ Make sure that content is written properly"""
        tmp = "/tmp"
        info = read_content(self.game_path)

        new_game = create_content(info, None, tmp)

        # dir and files are written properly
        self.assertTrue(os.path.isdir(new_game))
        json_path = os.path.join(new_game, "info.json")
        self.assertTrue(os.path.exists(json_path))

        new_game_info = read_content(new_game)

        # basic check for simlarity
        self.assertTrue(info["title"], new_game_info["title"])

        # make sure history has been written
        self.assertIn("history", new_game_info.keys())
        self.assertTrue(len(new_game_info["history"]), 1)
        event = new_game_info["history"][0]
        self.assertTrue(event["type"], "create")

    def test_create_content_invalid(self):
        """Make sure an error is raised before writing invalid data"""
        info = read_content(self.game_path)
        info_wrong = info.copy()
        info_wrong["description"] = 72
        self.assertRaises(ValidationError, lambda:create_content(info_wrong, None,self.tmp_path))

    def test_create_content_already_existing(self):
        tmp = "/tmp"
        info = read_content(self.game_path)

        new_game = create_content(info, None, tmp)
        self.assertRaises(LudoboxError, lambda : create_content(info, None, tmp))

    def test_delete_content(self):
        """Make sure the directory is erased properly"""
        os.makedirs(self.tmp_path) # create game path
        delete_content(self.tmp_path)
        self.assertFalse(os.path.exists(self.tmp_path))

    def test_update_content_info(self):
        tmp = "/tmp"
        info = read_content(self.game_path)

        game_path = create_content(info, None, tmp)
        game_info = read_content(game_path)

        new_game_info = game_info.copy()
        new_game_info["title"] = "bla bla bla"

        updated_content = update_content_info(game_path, new_game_info)
        self.assertEqual(len(updated_content["history"]), 2)
        event = updated_content["history"][1]
        self.assertEqual(event["type"], "update")

    # TODO : better config parameter to make this testable
    def test_get_content_index(self):

        print get_content_index()
        pass
        # self.assertTrue(False)
