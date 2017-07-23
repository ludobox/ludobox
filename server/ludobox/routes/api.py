#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from functools import wraps
import os
import sys
import json

from flask import Blueprint, abort

from flask import jsonify, send_from_directory, request, render_template, url_for, redirect, g, current_app

from flask_security import current_user
from ludobox.security import user_datastore

from datetime import datetime
from functools import update_wrapper

from ludobox import __version__

from ludobox.content import write_info_json, create_content, get_content_index, get_resource_slug, update_content_info

from ludobox.attachments import get_attachements_list

from ludobox.errors import LudoboxError
from ludobox.flat_files import create_resource_folder
from ludobox.data.crawler import download_from_server

from ludobox.config import read_config
from ludobox.user import get_latest_changes

# parse config
config = read_config()

# JSON API blueprint
rest_api = Blueprint('api', __name__)

def get_global_config():
    # get user info
    user = {
        'is_auth' : current_user.is_authenticated
    }
    if current_user.is_authenticated:
        user['email'] =  current_user.email
        user['username'] =  current_user.username
        user['roles'] =  [role.name for role in current_user.roles]

    return dict(
        name= config["ludobox_name"],
        version =  __version__,
        env = { "python" :  sys.version },
        config = config,
        user = user
    )

# login decorator for API
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated is False:
            return jsonify({"message" : "You need to log in to do that"}), 403
        return f(*args, **kwargs)
    return decorated_function

@rest_api.route('/api')
def api_show_home():
    return jsonify(get_global_config())

@rest_api.route('/api/create', methods=["POST"])
@login_required
def api_create_resource():
    """
    This function allow to post 2 things :

    * info : a dict containing a (valid) description of the game
    * files : a bunch of files of the game itself

    """

    # make sure unauthorized boxes can not create new games
    if current_app.config["UPLOAD_ALLOWED"] is False:
        response = jsonify({'message':'Upload not allowed'})
        return response, 401

    files = request.files.getlist('files')
    current_app.logger.debug("UPLOADED FILES:", [f.filename for f in files])

    info = json.loads(request.form["info"])

    # Save the game description as pure JSON file
    data_path = create_content(info, files, current_app.config["DATA_DIR"])

    slugified_name = get_resource_slug(info)

    return jsonify({"path" : data_path, "slug" : slugified_name}), 201

@rest_api.route('/api/update', methods=["POST"])
@login_required
def api_update_resource():
    """
    This function allow to post 2 things :

    * info : the dict containing the (valid) updated description of the game
    * slug : path/slug of the game

    """

    new_game_info = json.loads(request.form["info"])
    game_slug = json.loads(request.form["slug"])
    content_path = os.path.join(current_app.config["DATA_DIR"], game_slug)

    # make sure the game actually exists
    if not os.path.isdir(content_path):
        abort(404)

    new_info_with_history = update_content_info(content_path, new_game_info)

    return jsonify({
        "path" : content_path,
        "message" : "ok! Game %s has been updated."%new_game_info["title"],
        "updated_content" : new_info_with_history
        }), 201

@rest_api.route('/api/clone', methods=["POST"])
def api_clone_resource():
    """
    This function clone a resource
    it takes a valid JSON description of the game
    and will then proceed to the download the files.
    """
    # TODO : convert to decorator
    # make sure unauthorized boxes can not create new games
    if current_app.config["UPLOAD_ALLOWED"] is False:
        response = jsonify({'message':'Upload not allowed'})
        return response, 401

    data = request.get_json()

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
    return jsonify({"path" : content_path}), 201

@rest_api.route('/', defaults={'path': ''}, methods=['GET'])
@rest_api.route('/<path:path>', methods=['GET'])
def api_catch_all(path):
    """Serve the main page."""
    return render_template('index.html', initial_data=get_global_config())

# add unlimited CORS access
@rest_api.after_request
def api_add_cors(resp):
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
def api_handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
