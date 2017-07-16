#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json

from ludobox.content import read_content
from ludobox.routes.api import rest_api

# test helpers
from LudoboxTestCase import LudoboxTestCase
from helpers import delete_data_path, create_empty_data_path, add_samples_to_data_dir

class TestLudoboxWebServer(LudoboxTestCase):

    def setUp(self):

        # register routes
        self.app.register_blueprint(rest_api)

        # register a new user
        rv = self.register(
            email=self.user_email,
            password=self.user_password
            )

    def test_home_status_code(self):
        result = self.client.get('/')

        # assert the status code of the response (redirected)
        self.assertEqual(result.status_code, 200)

    def test_api_show_home(self):

        result = self.client.get('/api')
        self.assertEqual(result.status_code, 200)
        # self.assertEqual(json.loads(result.data), {"name" : self.config["ludobox_name"]})

    def test_upload_allowed(self):
        # self.login(email=self.user_email, password=self.user_password)
        self.app.config["UPLOAD_ALLOWED"] = False

        with self.client:
            self.login()
            result = self.client.post('/api/create',
                                    data={},
                                    content_type='multipart/form-data'
                                    )

            self.assertEqual(result.status_code, 401)

    def test_add_game_forbidden(self):
        """Make sure only logged in user can add content"""

        valid_info = self.borgia_info_content

        delete_data_path(self.app.config["DATA_DIR"])
        create_empty_data_path(self.app.config["DATA_DIR"])

        data = {
            'files': self.files,
            'info': json.dumps(valid_info)
        }

        with self.app.test_client() as c:

            result = c.post('/api/create',
                                    data=data,
                                    content_type='multipart/form-data'
                                    )

            print result.data
            self.assertEqual(result.status_code, 403)

    def test_api_create_content(self):

        # create empy path for data
        delete_data_path(self.tmp_path)
        create_empty_data_path(self.tmp_path)

        # load info without history
        valid_info = self.borgia_info_content

        data = {
            'files': self.files,
            'info': json.dumps(valid_info)
        }
        with self.client:
            self.login()
            result = self.client.post('/api/create',
                                    data=data,
                                    content_type='multipart/form-data'
                                    )
            print result.data
            self.assertEqual(result.status_code, 201)

            res = json.loads(result.data)
            self.assertIn("path", res.keys())

            # load JSON info data
            with open(os.path.join(res["path"], 'info.json'), 'r' )as  f:
                stored_info = json.load(f)
            self.assertEquals(stored_info["title"], valid_info["title"])

            # check for files
            written_filenames = os.listdir(os.path.join(res["path"], 'files'))
            self.assertEqual(written_filenames.sort(), [f[1] for f in data["files"]].sort())

    def test_save_history_with_user(self):
        """Make sure the reference to user is correctly saved in history"""

        # create empy path for data
        delete_data_path(self.tmp_path)
        create_empty_data_path(self.tmp_path)

        # load info without history
        valid_info = self.borgia_info_content

        data = {
            'files': self.files,
            'info': json.dumps(valid_info)
        }

        with self.client:
            self.login()

            # create the game through API
            result = self.client.post('/api/create',
                                    data=data,
                                    content_type='multipart/form-data'
                                    )
            self.assertEqual(result.status_code, 201)
            game_path = result.json["path"]

            # get the game content
            game_info = read_content(game_path)

            # check history event content
            self.assertEqual(len(game_info["history"]), 1)
            event = game_info["history"][0]
            self.assertEqual(event["type"], "create")
            self.assertEqual(event["user"], self.user_email)

            # make some changes to the data
            new_info = valid_info.copy()
            new_info["title"] = "bla bla bla"

            # post the update
            new_data = {
                'info' : json.dumps(new_info),
                'slug' : json.dumps(new_info["slug"])
            }
            result = self.client.post('/api/update',
                                    data=new_data,
                                    content_type='multipart/form-data'
                                    )

            self.assertEqual(result.status_code, 201)

            # read updated game
            game_path = result.json["path"]
            new_game_info = read_content(game_path)
            new_game_info["title"] = "bla bla bla"

            # check history event content
            self.assertEqual(len(new_game_info["history"]), 2)
            event = new_game_info["history"][1]
            self.assertEqual(event["type"], "update")
            self.assertEqual(event["user"], self.user_email)

    # def test_form_add_game(self):
    #     """Posting data and files using form should create a new game"""
    #
    #     # delete everything first
    #     clean(OUTPUT_DIR)
    #
    #     valid_info = read_content(os.path.join(os.getcwd(), 'server/tests/test-data/test-game'))
    #     data = {
    #         'files': self.files,
    #         'info': json.dumps(valid_info)
    #     }
    #
    #     result = self.client.post('/addgame',
    #                             data=data,
    #                             content_type='multipart/form-data'
    #                             )
    #
    #     # redirect
    #     self.assertEqual(result.status_code, 302)
    #
    #     path = '/tmp/data/borgia-le-jeu-malsain-fr'
    #
    #     # load JSON info data
    #     with open(os.path.join(path, 'info.json'), 'r' )as  f:
    #         stored_info = json.load(f)
    #     self.assertEqual(stored_info, valid_info)
    #
    #     # check for attached files
    #     written_filenames = os.listdir(os.path.join(path, 'files'))
    #     self.assertEqual(written_filenames.sort(), [f[1] for f in data["files"]].sort())
    #
    #     # HTML page created
    #     html_game_path = os.path.join(OUTPUT_DIR, os.path.join("games", 'borgia-le-jeu-malsain-fr'))
    #     print html_game_path
    #     self.assertTrue(os.path.exists(html_game_path))
    #     self.assertTrue(os.path.isdir(html_game_path))
    #     self.assertTrue(os.path.exists(os.path.join(html_game_path, 'index.html')))
