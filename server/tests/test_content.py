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

from ludobox.flat_files import write_info_json

from helpers import delete_data_path, create_empty_data_path, add_samples_to_data_dir

from LudoboxTestCase import LudoboxTestCase

from ludobox.content import get_content_type, validate_content, read_content, create_content, update_content_info, get_content_index, delete_content

TEST_DATA_DIR = '/tmp/test-data'

class TestLudoboxContent(LudoboxTestCase):
    """Functions to index, sort and search content"""

    def setUp(self):
        self.game_path = os.path.join(self.tmp_path,"test-game")
        delete_data_path('/tmp/game-borgia-le-jeu-malsain-fr')

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
        borgia_game_path = os.path.join(self.tmp_path, 'game-borgia-le-jeu-malsain-fr')
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
        self.assertEquals(info["slug"], "borgia-le-jeu-malsain-fr")

    def test_read_content_validation(self):
        """Wrong game should raises validation error"""


        wrong_content = self.borgia_info_content.copy()
        wrong_content["title"] = 345

        # create a bad record if needed
        wrong_game_path = os.path.join(TEST_DATA_DIR,"wrong-game")
        os.makedirs(wrong_game_path)
        write_info_json(wrong_content, wrong_game_path)

        self.assertRaises(ValidationError, lambda:read_content(wrong_game_path))

    def test_create_content_without_attachements(self):
        """ Make sure that content is written properly"""
        tmp = "/tmp"
        info = self.borgia_info_content

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
        info = self.borgia_info_content
        info_wrong = info.copy()
        info_wrong["description"] = 72
        self.assertRaises(ValidationError, lambda:create_content(info_wrong, None, self.tmp_path))

    def test_create_content_already_existing(self):
        tmp = "/tmp"
        info = self.borgia_info_content

        new_game = create_content(info, None, tmp)
        self.assertRaises(LudoboxError, lambda : create_content(info, None, tmp))

    def test_delete_content(self):
        """Make sure the directory is erased properly"""
        delete_content(self.tmp_path)
        self.assertFalse(os.path.exists(self.tmp_path))

    def test_update_content_info(self):
        tmp = "/tmp"
        info = self.borgia_info_content

        game_path = create_content(info, None, tmp)
        game_info = read_content(game_path)

        new_game_info = game_info.copy()
        new_game_info["title"] = "bla bla bla"

        updated_content = update_content_info(game_path, new_game_info)
        self.assertEqual(len(updated_content["history"]), 2)
        event = updated_content["history"][1]
        self.assertEqual(event["type"], "update")

    def test_create_slug_once_and_for_all(self):

        tmp = "/tmp"
        slug = "game-bla-bla-bla-fr"

        # clean
        delete_data_path(os.path.join(tmp, slug))

        info = self.borgia_info_content.copy()
        info["title"] = "bla bla bla"
        info.pop('slug', None) # remove slug

        self.assertRaises(KeyError, lambda : info["slug"])

        game_path = create_content(info, None, tmp)

        game_info = read_content(game_path)
        self.assertEqual(game_info["slug"], "game-bla-bla-bla-fr")

        new_game_info = info.copy()
        new_game_info["title"] = "bla bla bla 2"

        updated_content = update_content_info(game_path, new_game_info)
        self.assertEqual(slug,updated_content["slug"])
        self.assertEqual(game_info["slug"],updated_content["slug"])

    # TODO : better config parameter to make this testable
    # def test_get_content_index(self):
        # print get_content_index()
        # pass
        # self.assertTrue(False)
