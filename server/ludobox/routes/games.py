#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, abort, jsonify

from ludobox.content import get_content_index

# JSON API blueprint
games_api = Blueprint('game', __name__)

@games_api.route('/api/games')
def serve_games_json_index():
    games_index = get_content_index()
    return jsonify(games_index)

@games_api.route('/api/games/<path:path>')
def serve_rest_api(path):
    if path[-4:] == "json" :
        return send_from_directory('data', path, mimetype='application/json')
    else :
        return send_from_directory('data', path)
