#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from functools import wraps
import os
import sys
import json

from flask import Blueprint

from flask import jsonify, send_from_directory, request, render_template, url_for, redirect, g, current_app

from flask_login import current_user

from datetime import datetime
from functools import update_wrapper

from ludobox import __version__

from ludobox.content import write_info_json, create_content, get_content_index, get_resource_slug, update_content_info

from ludobox.attachments import store_files, delete_file, get_attachements_list

from ludobox.errors import LudoboxError
from ludobox.flat_files import create_resource_folder
from ludobox.data.crawler import download_from_server

from ludobox.config import read_config

# parse config
config = read_config()

# JSON API blueprint
rest_api = Blueprint('api', __name__)

# login decorator for API
def rest_api_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated is False:
            return jsonify({"message" : "You need to log in to do that"}), 403
        return f(*args, **kwargs)
    return decorated_function

@rest_api.route('/api')
def show_hand():
    return jsonify(
        name= config["ludobox_name"],
        version =  __version__,
        env = { "python" :  sys.version },
        config = config
    )

@rest_api.route('/api/schema/game')
def serve_schema():
    return send_from_directory('model', "game.json")

@rest_api.route('/api/games')
def serve_games_json_index():
    games_index = get_content_index()
    return jsonify(games_index)

@rest_api.route('/api/games/<path:path>')
def serve_rest_api(path):
    if path[-4:] == "json" :
        return send_from_directory('data', path, mimetype='application/json')
    else :
        return send_from_directory('data', path)

@rest_api.route('/api/files/<path:path>')
def serve_files_list(path):
    file_list = get_attachements_list(path)
    return jsonify(file_list)

@rest_api.route('/api/clone', methods=["POST"])
def clone_resource():
    """
    This function clone a resource
    it takes a valid JSON description of the game
    and will then proceed to the download the files.
    """
    # TODO : convert to decorator
    # make sure unauthorized boxes can not create new games
    if app.config["UPLOAD_ALLOWED"] is False:
        response = jsonify({'message':'Upload not allowed'})
        return response, 401

    data = request.get_json()
    print data

    info = data["info"]
    files_list = data["files"]
    slug = data["slug"]

    resource_path = os.path.join(app.config["DATA_DIR"], slug)
    if not os.path.exists(resource_path):
        create_resource_folder(resource_path)

    socket.emit("downloadEvent", {"slug" : slug, "message" : "Game path created." })

    # clone the JSON info
    write_info_json(info, resource_path)

    socket.emit("downloadEvent", {"slug" : slug, "message" : "Game info copied." })

    # make sub-rep to store files
    files_path = os.path.join(resource_path, "files")
    if not os.path.exists(files_path):
        os.makedirs(files_path)

    # download files from server
    for i, f in enumerate(files_list):
        socket.emit("downloadEvent", {
            "slug" : slug,
            "message" : "File %s/%s downloading..."%(i,len(files_list))
        })
        download_from_server(f["url"], files_path, f["filename"])
        socket.emit("downloadEvent", {
            "slug" : slug,
            "message" : "File %s/%s downloaded."%(i,len(files_list))
        })
    # return original JSON
    return jsonify({"path" : game_path}), 201

@rest_api.route('/api/create', methods=["POST"])
@rest_api_login_required
def create_resource():
    """
    This function allow to post 2 things :

    * info : a dict containing a (valid) description of the game
    * files : a bunch of files of the game itself

    """

    # make sure unauthorized boxes can not create new games
    if app.config["UPLOAD_ALLOWED"] is False:
        response = jsonify({'message':'Upload not allowed'})
        return response, 401

    files = request.files.getlist('files')
    print("UPLOADED FILES:", [f.filename for f in files])

    info = json.loads(request.form["info"])

    # Save the game description as pure JSON file
    data_path = create_content(info, files, app.config["DATA_DIR"])

    slugified_name = get_resource_slug(info)

    return jsonify({"path" : data_path, "slug" : slugified_name}), 201

@rest_api_login_required
@rest_api.route('/api/update', methods=["POST"])
def update_resource():
    """
    This function allow to post 2 things :

    * info : the dict containing the (valid) updated description of the game
    * slug : path/slug of the game

    """

    new_game_info = json.loads(request.form["info"])
    game_slug = json.loads(request.form["slug"])
    game_path = os.path.join(app.config["DATA_DIR"], game_slug)

    update_content_info(game_path, new_game_info)

    return jsonify({"message" : "ok! updated"}), 201

def get_file_list(game_path):
    files_path = os.path.join(game_path,"files")
    if os.path.exists(files_path):
        file_list = os.listdir(files_path)
    else :
        file_list = []
    return file_list

@rest_api_login_required
@rest_api.route('/api/postFiles', methods=["POST"])
def post_files():
    """
    This function allow to post 2 things :

    * files : an array of files
    * slug : path/slug of the game

    """

    files = request.files.getlist('files')
    print("UPLOADED FILES:", [f.filename for f in files])


    game_slug = json.loads(request.form["slug"])
    game_path = os.path.join(app.config["DATA_DIR"], game_slug)

    store_files(game_path, files)

    file_list =get_file_list(game_path)
    return jsonify({"message" : "files added", "files" : file_list }), 201

@rest_api_login_required
@rest_api.route('/api/deleteFile', methods=["POST"])
def delete_files():

    to_delete = json.loads(request.form["toDelete"])
    print to_delete

    game_path = os.path.join(app.config["DATA_DIR"], to_delete["slug"])
    to_delete_path = os.path.join(os.path.join(game_path, "files"), to_delete["fileName"])
    print to_delete_path

    delete_file(to_delete_path)

    file_list =get_file_list(game_path)

    return jsonify({"message" : "files added", "files" : file_list }), 203

@rest_api.route('/', defaults={'path': ''}, methods=['GET'])
@rest_api.route('/<path:path>', methods=['GET'])
def catch_all(path):
    """Serve the main page."""
    return render_template('index.html')

# add unlimited CORS access
@rest_api.after_request
def add_cors(resp):
    """ Ensure all responses have the CORS headers. This ensures any failures are also ccessible
         by the client. """
    resp.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin','*')
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET'
    resp.headers['Access-Control-Allow-Headers'] = request.headers.get(
    'Access-Control-Request-Headers', 'Authorization' )
    # set low for debugging
    if current_app.debug:
        resp.headers['Access-Control-Max-Age'] = '1'
    return resp

# register error handler
@rest_api.errorhandler(LudoboxError)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
