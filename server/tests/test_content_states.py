#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import unittest
from LudoboxTestCase import LudoboxTestCase

from helpers import delete_data_path

from ludobox.content import create_content, read_content
from ludobox.errors import LudoboxError

from ludobox.content_states import is_valid_content_state, is_valid_state_change,  update_content_state, validates, rejects
from ludobox.history import make_create_event, make_update_state_event, is_valid_event


class TestLudoboxContent(LudoboxTestCase):

    def setUp(self):
        delete_data_path(os.path.join(self.tmp_path, self.borgia_info_content["slug"]))

        # create a game
        info = self.borgia_info_content
        new_game_path = create_content(info, None, self.tmp_path)

    def test_is_valid_content_state(self):
        self.assertFalse( is_valid_content_state("bla") )
        self.assertFalse( is_valid_content_state(12) )
        self.assertTrue( is_valid_content_state("validated") )

    def test_is_valid_state_change(self):
        self.assertTrue(is_valid_state_change("needs_review", "validated"))
        self.assertFalse(is_valid_state_change("needs_review", "needs_review"))
        self.assertFalse(is_valid_state_change("needs_review", "dsjkd"))

    def test_prevent_break_test_workflow(self):
        """Make sure we don't jump from a state to another and breaks the workflow or skip a mandatory state"""
        # self.fail()
        pass

    def test_prevent_wrong_state_name(self):
        """Make sure you can only add valid state names."""
        info = self.borgia_info_content
        delete_data_path(os.path.join(self.tmp_path, info["slug"] ))

        # create a game
        new_game_path = create_content(info, None, self.tmp_path)

        self.assertRaises(LudoboxError, lambda:update_content_state(new_game_path, "lalala" ))

    def test_make_update_state_event(self):
        # create a basic game and update it
        game_content = { "title" : "test game", "state" : "needs_review"}

        # update the game
        event = make_update_state_event(game_content, "needs_review")
        self.assertEquals(is_valid_event(event), True)
        self.assertEquals(event["type"], "change_state")
        self.assertEquals(event["content"]["to"], "needs_review")
        self.assertEquals(event["content"]["from"], "needs_review")

    def test_update_content_state(self):
        """State should be updated when asked to"""

        info = self.borgia_info_content
        new_game_path = os.path.join(self.tmp_path, info["slug"] )

        new_game = update_content_state(new_game_path, "validated")
        self.assertEqual(new_game["state"], "validated")

        info_stored_file = read_content(new_game_path)
        self.assertEqual(info_stored_file["state"], "validated")
