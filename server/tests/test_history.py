#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from ludobox.history import new_event, is_valid_event, add_event_to_history, make_create_event, make_update_event, apply_history

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

    def test_make_create_event(self):
        """Check that content is created properly"""

        # return empty value when content is empty
        empty_content = make_create_event({})
        self.assertEquals(empty_content, None)

        game_content = { "title" : "test game"}
        event = make_create_event(game_content)
        self.assertEquals( is_valid_event(event), True)
        self.assertEquals( event["type"], "create")
        self.assertEquals( event["content"], game_content)

    def test_make_create_event_reject_games_with_prior_history(self):
        """make_create_event should not tolerate games with prior history"""
        game = {"title" :"test", "history" : [1]}
        self.assertRaises(ValueError, lambda :make_create_event(game))

    def test_update_content(self):
        """Content update should be stored using ISO json diff"""

        # create a basic game and update it
        game_content = { "title" : "test game"}
        new_game_content = { "title" : "My test game"}

        creation = make_create_event(game_content)
        created_game = add_event_to_history({}, creation)

        # make sure we pass the content *without* the history
        self.assertRaises(ValueError, lambda : make_update_event(new_game_content, created_game))

        # update the game
        event = make_update_event(game_content, new_game_content)
        self.assertEquals(is_valid_event(event), True)
        self.assertEquals(event["type"], "update")
        self.assertEquals(type(event["content"]["changes"]), list)
        self.assertEquals(len(event["content"]["changes"]), 1)
        self.assertEquals(event["content"]["changes"][0]["value"], "My test game")
        self.assertEquals(event["content"]["changes"][0]["op"], "replace")

    def test_apply_history(self):
        """
        Course of events should change history
        and should also changed the actual content.
        -- very deep thoughts here :)
        """

        game_content = { "title" : "test game"}
        creation = make_create_event(game_content)
        created_game = add_event_to_history(game_content, creation)

        new_game_content_1 = { "title" : "My test game"}
        update1 = make_update_event(game_content, new_game_content_1)
        updated_game = add_event_to_history(created_game, update1)

        self.assertEquals(updated_game["title"], new_game_content_1["title"])

        new_game_content_2 = {
            "title" : "My test game",
            "description" : "An awesome game"
        }
        update2 = make_update_event(game_content, new_game_content_2)
        updated_game = add_event_to_history(updated_game, update2)

        self.assertTrue("description" in updated_game.keys())

        new_game_content_3 = {
            "title" : "My final test game",
            "description" : "A very awesome game",
            "fab_time" : 120
            }
        update3 = make_update_event(game_content, new_game_content_3)
        updated_game = add_event_to_history(updated_game, update3)

        self.assertTrue("fab_time" in updated_game.keys())
        self.assertEquals(updated_game["title"], new_game_content_3["title"])

        # assert that the whole history is there
        self.assertEquals(len(updated_game["history"]), 4)
        self.assertEquals(updated_game["title"], "My final test game")

        # let's check if we can rewrite history
        ids = [ event["id"] for event in updated_game["history"]]

        step_zero = apply_history(updated_game["history"], ids[0])
        self.assertDictEqual(game_content, step_zero)
        step_one = apply_history(updated_game["history"], ids[1])
        self.assertDictEqual(new_game_content_1, step_one)
        step_two = apply_history(updated_game["history"], ids[2])
        self.assertDictEqual(new_game_content_2, step_two)
        step_three = apply_history(updated_game["history"], ids[3])
        self.assertDictEqual(new_game_content_3, step_three)
