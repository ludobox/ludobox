#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import unittest
from datetime import datetime

from jsonpatch import make_patch, JsonPatch

from ludobox.config import read_config
from ludobox.content import read_game_info, validate_game_data, update_game_info
from ludobox.utils import json_serial

class TestLudoboxUpdateContent(unittest.TestCase):
    """Functions to edit/update/store edits of game contents"""

    def setUp(self):
        self.config = read_config()
        self.game_path = os.path.join(os.getcwd(), 'server/tests/test-data/test-game')

    def test_basic_game_info_update(self):
        """Make sure an update is properly parsed and stored"""
        borgia_game_path = os.path.join(os.getcwd(), 'data/borgia-le-jeu-malsain')
        print borgia_game_path

        borgia_info = read_game_info(borgia_game_path)

        # make some basic changes
        modified_borgia_info = borgia_info
        modified_borgia_info["title"] = "Coucou"

        updated_game_info = update_game_info(borgia_game_path, modified_borgia_info)

        # make sure there is a new event in history
        self.assertEquals(len(updated_game_info["history"]), 1)

        event = updated_game_info["history"][0]["patch"]
        print event

        # try to apply patch again
        new = JsonPatch(event).apply(borgia_info)
        print new
        patch = make_patch(new, modified_borgia_info)
        self.assertEquals(len(list(patch)), 0) #make sure there is no difference

    def test_validate_basic_event_history(self):

        borgia_game_path = os.path.join(os.getcwd(), 'data/borgia-le-jeu-malsain')
        print borgia_game_path

        borgia_info = read_game_info(borgia_game_path)

        # make some basic changes
        modified_borgia_info = borgia_info
        modified_borgia_info["title"] = "Coucou"

        updated_game_info = update_game_info(borgia_game_path, modified_borgia_info)

        validate_game_data(updated_game_info)
