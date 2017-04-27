#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

import os
import sys
import json
from flask import Flask, jsonify, send_from_directory, request, render_template, url_for, redirect

from datetime import datetime
from functools import update_wrapper

from ludobox import __version__

from ludobox.config import read_config
from ludobox.content import create_game_path, write_info_json, write_game, validate_game_data, get_games_index, get_resource_slug
from ludobox.errors import LudoboxError
from ludobox.data.crawler import download_from_server
from ludobox.socketio import socket

# parse config
config = read_config()

tmpl_dir = os.path.join(os.path.join(os.getcwd(), 'server'), 'templates')
app = Flask("LUDOSERVER", template_folder=tmpl_dir)  # web server instance used to defines routes

# config
app.config["DATA_DIR"] = config["data_dir"] # used for testing
print "Data will be stored at %s"%app.config["DATA_DIR"]

app.config["UPLOAD_ALLOWED"] = config["upload_allowed"] # used for testing
print "Upload allowed : %s"%app.config["UPLOAD_ALLOWED"]

socket.init_app(app)

# STATIC FILES
@app.route('/js/<path:path>')
def serve_js(path):
    return send_from_directory('public/js', path)

@app.route('/css/<path:path>')
def serve_css(path):
    return send_from_directory('public/css', path)

@app.route('/images/<path:path>')
def serve_images(path):
    return send_from_directory('public/images', path)

# API Calls
@app.route('/api')
def show_hand():
    return jsonify(
        name= config["ludobox_name"],
        version =  __version__,
        env = { "python" :  sys.version },
        config = config
    )

@app.route('/api/schema')
def serve_schema():
    return send_from_directory('model', "schema.json")

@app.route('/api/games')
def serve_games_json_index():
    games_index = get_games_index()
    return jsonify(games_index)

@app.route('/api/games/<path:path>')
def serve_api(path):
    if path[-4:] == "json" :
        return send_from_directory('data', path, mimetype='application/json')
    else :
        return send_from_directory('data', path)

@app.route('/api/files/<path:path>')
def serve_files_list(path):
    files_path = os.path.join("data", os.path.join(path,"files"))
    if os.path.exists(files_path):
        file_list = os.listdir(files_path)
    else :
        file_list = []
    return jsonify(file_list)

@app.route('/api/clone', methods=["POST"])
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

    game_path = os.path.join(app.config["DATA_DIR"], slug)
    if not os.path.exists(game_path):
        create_game_path(game_path)

    socket.emit("downloadEvent", {"slug" : slug, "message" : "Game path created." })

    # clone the JSON info
    write_info_json(info, game_path)

    socket.emit("downloadEvent", {"slug" : slug, "message" : "Game info copied." })

    # make sub-rep to store files
    files_path = os.path.join(game_path, "files")
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

@app.route('/api/create', methods=["POST"])
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
    data_path = write_game(info, files, app.config["DATA_DIR"])

    slugified_name = get_resource_slug(info)

    return jsonify({"path" : data_path, "slug" : slugified_name}), 201


@app.route('/', defaults={'path': ''}, methods=['GET'])
@app.route('/<path:path>', methods=['GET'])
def catch_all(path):
    """Serve the main page."""
    return render_template('index.html')

# add unlimited CORS access
@app.after_request
def add_cors(resp):
    """ Ensure all responses have the CORS headers. This ensures any failures are also ccessible
         by the client. """
    resp.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin','*')
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET'
    resp.headers['Access-Control-Allow-Headers'] = request.headers.get(
    'Access-Control-Request-Headers', 'Authorization' )
    # set low for debugging
    if app.debug:
        resp.headers['Access-Control-Max-Age'] = '1'
    return resp


# register error handler
@app.errorhandler(LudoboxError)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
