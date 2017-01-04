#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from flask import Flask, jsonify, redirect, send_from_directory, request, url_for

from ludobox.config import read_config
from ludobox.content import write_game, validate_game_data
from ludobox.errors import LudoboxError
from ludobox.core import generate_all, OUTPUT_DIR

# parse config
config = read_config()

app = Flask("LUDOSERVER")  # web server instance used to defines routes

# config
app.config["DATA_DIR"] = config["data_dir"] # used for testing
print "Data will be stored at %s"%app.config["DATA_DIR"]

app.config["UPLOAD_ALLOWED"] = config["upload_allowed"] # used for testing
print "Upload allowed : %s"%app.config["UPLOAD_ALLOWED"]


def serve(debug, **kwargs):
    """
    Launch an tiny web server to make the ludobox site available.

    Keyword arguments:
    debug -- bool to activate the debug mode of the Flask server (for
             development only NEVER use it in production).

    kwargs is used here since this function is called by :func:`main` via
    :mod:`argparse`. And all the params are provided automagically by
    :func:`argparse.ArgumentParser.parse_args` converted to a dict using
    :func:`vars`.
    See `Namespace object<https://docs.python.org/2/library/argparse.html#the-namespace-object>`_
    """

    app.run(host='0.0.0.0', port=config["port"], debug=debug)

@app.route('/')
def serve_index():
    """Serve the base url for the project."""
    return redirect(url_for("static", filename="index.html"))

@app.route('/api/<path:path>')
def serve_api(path):
    return send_from_directory('data', path)

@app.route('/api')
def show_hand():
    return jsonify( name= config["ludobox_name"] )

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

    info = json.loads(request.form["info"])
    files = request.files.getlist('files')

    print("UPLOADED FILES:", [f.filename for f in files])

    # Save the game description as pure JSON file
    data_path = write_game(info, files, app.config["DATA_DIR"])

    # try:
    #     # TODO handle API exceptions properly
    # except LudoboxError as e:
    #     # TODO replace this dummy return by a true page showing the failed add
    #     return redirect(url_for("static", filename="index.html"))

    # return original JSON
    return jsonify({"path" : data_path}), 201


@app.route('/addgame', methods=["POST"])
def serve_addgame():
    """Process the uploads of new games."""

    if app.config["UPLOAD_ALLOWED"] is False:
        return redirect(url_for("static", filename="index.html"))

    # get and parse content
    info = json.loads(request.form["info"])
    files = request.files.getlist('files')

    try:
        # TODO split this in 2 funcs "write json" and "write attachements"
        data_path = write_game(info, files, app.config["DATA_DIR"])
    except LudoboxError as e:
        # TODO replace this dummy return by a true page showing the failed add
        return redirect(url_for("static", filename="index.html"))

    # Generate the HTML pages !
    if not generate_all(app.config["DATA_DIR"], OUTPUT_DIR):
        # TODO replace this dummy return by a true page showing the failed gen
        return redirect(url_for("static", filename="index.html"))

    # TODO replace this dummy return by a true page showing the successful add
    return redirect(url_for("static", filename="index.html"))
