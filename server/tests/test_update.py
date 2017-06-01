#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import unittest
from datetime import datetime

import tempfile, shutil
import uuid

from jsonpatch import make_patch, JsonPatch

from ludobox.config import read_config
from ludobox.content import read_game_info, validate_game_data, update_game_info, write_info_json
from ludobox.utils import json_serial

def create_temporary_copy(path):
    temp_dir = tempfile.gettempdir()
    temp_file_name = str(uuid.uuid4())
    temp_path = os.path.join(temp_dir, temp_file_name)
    shutil.copytree(path, temp_path)
    return temp_path

class TestLudoboxUpdateContent(unittest.TestCase):
    """Functions to edit/update/store edits of game contents"""

    def setUp(self):
        self.config = read_config()
        self.game_path = os.path.join(os.getcwd(), 'server/tests/test-data/test-game')

        # load borgia data
        self.borgia_game_path = create_temporary_copy(
            os.path.join(os.getcwd(), 'data/borgia-le-jeu-malsain-fr')
        )
        print self.borgia_game_path

    def tearDown(self):
        # write clean
        shutil.rmtree(self.borgia_game_path)

    def test_basic_game_info_update(self):
        """Make sure an update is properly parsed and stored"""

        borgia_info = read_game_info(self.borgia_game_path)

        # make some basic changes
        modified_borgia_info = borgia_info
        modified_borgia_info["title"] = "Coucou"

        updated_game_info = update_game_info(self.borgia_game_path, modified_borgia_info)

        # make sure changes have been done
        self.assertEquals(modified_borgia_info["title"], updated_game_info["title"])
        self.assertEquals(updated_game_info["title"], "Coucou")

        # make sure there is a new event in history
        self.assertEquals(len(updated_game_info["history"]), 1)

        event = updated_game_info["history"][0]["patch"]
        print event

        # try to apply patch again
        new = JsonPatch(event).apply(modified_borgia_info)

        # make sure the original title is back
        self.assertEquals(new["title"], "Borgia, le jeu malsain")

    def test_validate_basic_event_history(self):

        borgia_info = read_game_info(self.borgia_game_path)

        # make some basic changes
        modified_borgia_info = borgia_info
        modified_borgia_info["title"] = "Coucou"

        updated_game_info = update_game_info(self.borgia_game_path, modified_borgia_info)

        validate_game_data(updated_game_info)

    def test_rename_game(self):
        """To rename a game should rename the folder as well"""

        # rename_game
