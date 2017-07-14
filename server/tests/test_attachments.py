#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest

from ludobox.config import read_config
from ludobox.attachments import write_attachments, allowed_file, get_attachements_list

class TestLudoboxAttachements(unittest.TestCase):
    """Functions to write/delete attachments"""

    def setUp(self):
        self.config = read_config()
        self.game_path = os.path.join(os.getcwd(), 'server/tests/test-data/test-game')

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

    def test_file_list(self):
        """retrieve a list of files from the '/files' forlder"""
        file_list = get_attachements_list(self.game_path)
        self.assertEquals(len(file_list), 1)
        self.assertEquals(file_list[0], "file1.txt")

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
