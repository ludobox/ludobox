#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest

from ludobox.attachments import write_attachments


# class TestLudoboxAttachements(unittest.TestCase):
#     """Functions to write/delete attachments"""
#


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
