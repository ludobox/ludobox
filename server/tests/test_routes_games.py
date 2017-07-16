#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
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
        data = json.loads(result.data)
        self.assertIs(type(data), list)
        self.assertTrue(type(data[0]), dict)
