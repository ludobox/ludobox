#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ludobox.routes.api import rest_api
from ludobox.routes.games import games_api

# test helpers
from LudoboxTestCase import LudoboxTestCase

class TestLudoboxGamesServer(LudoboxTestCase):

    def setUp(self):

        # register routes
        self.app.register_blueprint(rest_api)
        self.app.register_blueprint(games_api)

        # register a new user
        rv = self.register(
            email=self.user_email,
            password=self.user_password
            )

    def test_game_index(self):
        result = self.client.get('/api/games')
        data = result.json
        self.assertIs(type(data), list)
        self.assertTrue(type(data[0]), dict)
        self.assertEqual(len(data), 2)

    def test_single_game(self):
        info = self.borgia_info_content
        print self.app.config["DATA_DIR"]
        result = self.client.get('/api/games/%s'%info["slug"])
        data = result.json
        print data

        self.assertIn("Content-Type: application/json", str(result.headers))
        self.assertIs(type(data), dict)
        self.assertEqual(data["slug"], info["slug"])

    def test_get_game_that_does_not_exist(self):
        result = self.client.get('/api/games/some-slug"')
        self.assertEqual(result.status_code, 404)


    def test_delete_game(self):
        """Make sure the game is deleted properly"""
        info = self.borgia_info_content
        print self.app.config["DATA_DIR"]

        result = self.client.get('/api/games/%s'%info["slug"])
        self.assertEqual(result.status_code, 200)

        result = self.client.delete('/api/games/%s'%info["slug"])
        print result.data
        self.assertEqual(result.status_code, 203)
        self.assertIn("deleted", result.json["message"])

        result = self.client.get('/api/games/%s'%info["slug"])
        self.assertEqual(result.status_code, 404)
