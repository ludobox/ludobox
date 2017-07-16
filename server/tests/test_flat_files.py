#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import shutil
import unittest

from ludobox.errors import LudoboxError
from ludobox.flat_files import create_resource_folder, write_info_json, delete_resource_folder, read_info_json

class TestLudoboxFlatFileSystem(unittest.TestCase):
    """Functions to write/delete attachments"""

    def setUp(self):
        self.path = "/tmp/my-game"
        if os.path.exists(self.path):
            shutil.rmtree(self.path, ignore_errors=True)

    def test_create_resource_folder(self):

        create_resource_folder(self.path)
        self.assertTrue(os.path.isdir(self.path))

        # impossible to write if already exists
        self.assertRaises(LudoboxError, lambda : create_resource_folder(self.path))

    def test_delete_resource_folder(self):

        create_resource_folder(self.path)
        self.assertTrue(os.path.isdir(self.path))

        delete_resource_folder(self.path)
        self.assertTrue(not os.path.isdir(self.path))

    def test_write_info_json(self):
        path = "/tmp/my-game"
        create_resource_folder(path)
        self.assertTrue(os.path.isdir(path))

        info = {"title" : "some game", "description" : "some stuff"}

        write_info_json(info, self.path)
        json_path = os.path.join(self.path, "info.json")
        self.assertTrue(os.path.exists(json_path))

        # make sure data is written properly
        with open(json_path, 'r') as json_file :
            data = json.load(json_file)
        self.assertDictEqual(data, info)


    def test_read_info_json(self):
        path = "/tmp/my-game"
        create_resource_folder(path)
        self.assertTrue(os.path.isdir(path))

        info = {"title" : "some game", "description" : "some stuff"}

        write_info_json(info, self.path)
        json_path = os.path.join(self.path, "info.json")
        self.assertTrue(os.path.exists(json_path))

        data = read_info_json(self.path)
        self.assertDictEqual(data, info)
