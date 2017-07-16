#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from flask_security import current_user, url_for_security

import os
import json

from ludobox.routes.api import rest_api
from ludobox.routes.files import files_api

# test helpers
from LudoboxTestCase import LudoboxTestCase
from helpers import delete_data_path, create_empty_data_path, add_samples_to_data_dir

class TestLudoboxFilesServer(LudoboxTestCase):

    def setUp(self):
        # register routes
        self.app.register_blueprint(rest_api)
        self.app.register_blueprint(files_api)

        # register a new user
        rv = self.register(
            email=self.user_email,
            password=self.user_password
            )

    def test_api_serve_files_list_with_no_files(self):
        """API shoud returns an empty file if no files in the folder"""
        result = self.client.get('/api/files/dsdqdqs')
        data = json.loads(result.data)
        self.assertEquals(data, [])

    def test_api_serve_files_list_with_actual_files(self):
        """API shoud returns a list of files located in the /files folder"""
        with self.client as c:
            result = c.get('/api/files/test-game')
            data = result.json
            print data
            self.assertEquals(len(data), 1)
            self.assertEquals(data, ["file1.txt"])

    def test_post_multiple_files(self):
        """Make sure we can post multiple files at once"""
        slug = self.borgia_info_content["slug"]

        data = {
            'files': self.files,
            'slug': json.dumps(slug)
        }
        result = self.client.post('/api/files',
                                data=data,
                                content_type='multipart/form-data'
                                )
        self.assertEquals(len(result.json["files"]), 3)
        self.assertIn("files added", result.json["message"])

        files_path = os.path.join(os.path.join(self.tmp_path, slug), "files")
        files_list = os.listdir(files_path)
        self.assertEquals(len(files_list), 3)

    def test_delete_files_that_does_not_exist(self):
        """Make sure we can only delete files that exists"""
        result = self.client.delete('/api/files/blalba/blibib.jpg')
        print result.data
        self.assertEqual(result.status_code, 404)

    def test_delete_files(self):
        """Make sure we can delete a file"""
        slug = self.borgia_info_content["slug"]

        data = {
            'files': self.files,
            'slug': json.dumps(slug)
        }
        result = self.client.post('/api/files',
                                data=data,
                                content_type='multipart/form-data'
                                )
        self.assertEquals(len(result.json["files"]), 3)
        self.assertIn("files added", result.json["message"])

        files_path = os.path.join(os.path.join(self.tmp_path, slug), "files")
        to_delete = os.path.join(files_path, self.files[0][1])

        print to_delete
        # make sure the file actually exists
        self.assertTrue(os.path.isfile(to_delete))

        url = '/api/files/%s/%s'%(slug,self.files[0][1])
        result = self.client.delete(url)

        self.assertFalse(os.path.isfile(to_delete))
        self.assertEquals(len(result.json["files"]), 2)
        self.assertIn("deleted", result.json["message"])
        self.assertIn(self.files[0][1], result.json["message"])
