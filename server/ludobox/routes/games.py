#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Blueprint, abort, jsonify, send_from_directory, current_app

from ludobox.content import get_content_index, read_content

# JSON API blueprint
games_api = Blueprint('game', __name__)

@games_api.route('/api/games')
def serve_games_json_index():
    games_index = get_content_index()
    return jsonify(games_index)

@games_api.route('/api/games/<path:path>')
def serve_rest_api(path):
    game_path = os.path.join(current_app.config["DATA_DIR"], path)
    content = read_content(game_path)
    return jsonify(content)
