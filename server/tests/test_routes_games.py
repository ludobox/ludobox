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

    def test_single_game(self):
        info = self.borgia_info_content

        result = self.client.get('/api/games/%s/info.json'%info["slug"])
        data = result.json

        self.assertIn("Content-Type: application/json", str(result.headers))
        self.assertIs(type(data), dict)
        self.assertEqual(data["slug"], info["slug"])
