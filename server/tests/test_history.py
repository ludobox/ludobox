#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from ludobox.history import new_event, is_valid_event, add_event_to_history, event_create, event_update

class TestLudoboxContent(unittest.TestCase):
    """Functions to index, sort and search content"""

    def setUp(self):
        self.content = { "bla" : "bla" }

    def test_new_event_type(self):
        """A new event should have a validated type"""

        # works with proper event type
        event = new_event("update", {})
        self.assertEquals(event["type"], "update")

        # catch wrong event type
        self.assertRaises(ValueError, lambda:new_event("sth", {}))

        # content should be a JSON dict
        self.assertRaises(ValueError, lambda:new_event("create", []))

    def test_new_event_unique_id(self):
        """A new event should have a unique id"""

        event = new_event("create", {})
        self.assertEquals(type(event["id"]), str)
        self.assertEquals(len(event["id"]), 40) # sha_id hexdigest

    def test_is_valid_event(self):
        """Make sure event is correctly formatted"""
        fake_event = {
            "id" : "haha",
            "content" : []
        }
        self.assertRaises(KeyError, lambda:is_valid_event({}))
        self.assertRaises(AssertionError, lambda:is_valid_event(fake_event))

        normal_event = new_event("create", {})
        is_valid_event(normal_event)

    def test_add_event_to_history(self):
        """Make sure each event is properly added to history, starting with the oldest to the newest"""

        event = new_event("create", {})

        # create from scratch
        game_info = add_event_to_history({}, event)
        self.assertTrue("history" in game_info.keys())
        self.assertEquals(len(game_info["history"]),1)

        # add to existing array
        game_info = add_event_to_history({"history" : [1,2,3]}, event)
        self.assertEquals(len(game_info["history"]),4)

    def test_event_create(self):
        """Check that content is created properly"""

        # return empty value when content is empty
        empty_content = event_create({})
        self.assertEquals(empty_content, None)

        game_content = { "title" : "test game"}
        event = event_create(game_content)
        self.assertEquals( is_valid_event(event), True)
        self.assertEquals( event["type"], "create")
        self.assertEquals( event["content"], game_content)

    def test_event_create_reject_games_with_prior_history(self):
        """event_create should not tolerate games with prior history"""
        game = {"title" :"test", "history" : [1]}
        self.assertRaises(ValueError, lambda :event_create(game))

    def test_update_content(self):
        """Content update should be stored using ISO json diff"""

        # create a basic game and update it
        game_content = { "title" : "test game"}
        new_game_content = { "title" : "My test game"}

        creation = event_create(game_content)
        created_game = add_event_to_history({}, creation)

        # make sure we pass the content *without* the history
        self.assertRaises(ValueError, lambda : event_update(new_game_content, created_game))

        # update the game
        event = event_update(game_content, new_game_content)
        self.assertEquals(is_valid_event(event), True)
        self.assertEquals(event["type"], "update")
        self.assertEquals(type(event["content"]["changes"]), list)
        self.assertEquals(len(event["content"]["changes"]), 1)
        self.assertEquals(event["content"]["changes"][0]["value"], "My test game")
        self.assertEquals(event["content"]["changes"][0]["op"], "replace")
        print event

        self.assertTrue(False)
