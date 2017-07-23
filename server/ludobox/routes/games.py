#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Blueprint, abort, jsonify, send_from_directory, current_app

from flask_security.decorators import roles_accepted

from ludobox.content import get_content_index, read_content, delete_content
from ludobox.content_states import validates, back_to_review, rejects

from api import login_required

# JSON API blueprint
games_api = Blueprint('game', __name__)

@games_api.route('/api/games', methods=["GET"])
def api_games_index():
    games_index = get_content_index()
    return jsonify(games_index)

@games_api.route('/api/games/<path:path>', methods=["GET"])
def api_single_game(path):
    game_path = os.path.join(current_app.config["DATA_DIR"], path)
    if not os.path.exists(game_path):
        abort(404)
    content = read_content(game_path)
    return jsonify(content)

@games_api.route('/api/games/<path:path>', methods=["DELETE"])
@login_required
@roles_accepted("editor","superuser")
def api_delete_game(path):
    game_path = os.path.join(current_app.config["DATA_DIR"], path)
    content = delete_content(game_path)
    return jsonify({
        "message" : "Success : file %s deleted"%game_path
    }), 203

@games_api.route('/api/validates/<path:path>', methods=["POST"])
@login_required
@roles_accepted("editor","superuser")
def api_validates_game(path):
    game_path = os.path.join(current_app.config["DATA_DIR"], path)
    content = validates(game_path)
    return jsonify({
        "message" : "Success : file %s deleted"%game_path
    }), 203

@games_api.route('/api/back_to_review/<path:path>', methods=["POST"])
@login_required
@roles_accepted("editor","superuser")
def api_back_to_review_game(path):
    game_path = os.path.join(current_app.config["DATA_DIR"], path)
    content = back_to_review(game_path)
    return jsonify({
        "message" : "Success : file %s deleted"%game_path
    }), 203

@games_api.route('/api/rejects/<path:path>', methods=["POST"])
@login_required
@roles_accepted("editor","superuser")
def api_rejects_game(path):
    game_path = os.path.join(current_app.config["DATA_DIR"], path)
    content = rejects(game_path)
    return jsonify({
        "message" : "Success : file %s deleted"%game_path
    }), 203
