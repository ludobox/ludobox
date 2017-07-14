#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest

import io
from StringIO import StringIO

from ludobox.errors import LudoboxError
from ludobox.config import read_config
from ludobox.attachments import write_attachments, allowed_extension, get_attachements_list, check_attachments

class TestLudoboxAttachements(unittest.TestCase):
    """Functions to write/delete attachments"""

    def setUp(self):
        self.config = read_config()
        self.game_path = os.path.join(os.getcwd(), 'server/tests/test-data/test-game')

    def test_allowed_extensions(self):
        """Check if filenames are allowed"""
        self.assertTrue(allowed_extension("bla.txt"))
        self.assertTrue(allowed_extension("bla.png"))
        self.assertTrue(allowed_extension("bla.jpg"))
        self.assertTrue(allowed_extension("bla.gif"))
        self.assertTrue(allowed_extension("bla.stl"))
        self.assertTrue(allowed_extension("bla.zip"))
        self.assertFalse(allowed_extension("bla.xxx"))
        self.assertFalse(allowed_extension("bla.123"))

    def test_get_attachements_list(self):
        """retrieve a list of files from the '/files' forlder"""
        file_list = get_attachements_list(self.game_path)
        self.assertEquals(len(file_list), 1)
        self.assertEquals(file_list[0], "file1.txt")


    # def test_check_attachments(self):
    #     """Make sure we can upload only secure files"""
    #
    #     with io.open("/tmp/test.jpg", 'w', encoding='utf-8') as f:
    #         for i in xrange(10):
    #             f.write(unicode(i))
    #
    #     self.assertRaises(LudoboxError, check_attachments(test_files))

# TODO : find a way to test without Flask (tested in test_webserver.py anyway)
# def test_write_attachments(self):
#     """Make sure attachments are saved properly"""
#

#
#     # create game path
#     os.makedirs(self.tmp_path)
#
#     write_attachements(test_files, self.tmp_path)
# test_files = [
#     (StringIO('my readme'), 'test-README.txt'),
#     (StringIO('my rules'), 'test-RULES.docx'),
#     (io.BytesIO(b"abcdef"), 'test.jpg')
# ]
