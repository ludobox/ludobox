#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
from flask import Flask, jsonify, send_from_directory, request, render_template, make_response, current_app

from datetime import datetime
from functools import update_wrapper

from ludobox import __version__

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

def serve(debug, port, **kwargs):
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

    # check if port number is ok
    if port is None : _port = config["port"]
    else : _port = int(port)

    app.run(host='0.0.0.0', port=_port, debug=debug)

# TODO : optimize by pre-building files
@app.route('/')
def serve_intro():
    """Serve the intro page."""
    return render_template('intro.html')

@app.route('/create')
def serve_create():
    """Create a new game."""
    return render_template('add.html')

@app.route('/download')
def serve_download_index():
    """List of available games."""
    return render_template('download.html', remote_server_url=config["web_server_url"] )

@app.route('/about')
def serve_about():
    """Show the about page."""
    return render_template('about.html')

@app.route('/games')
def serve_index():
    """Serve the games index."""
    return render_template('index.html')

# catch all
@app.route('/games/<path:path>')
def serve_game(path):
    return render_template('single.html')

# STATIC FILES
@app.route('/js/<path:path>')
def serve_js(path):
    return send_from_directory('static/js', path)

@app.route('/css/<path:path>')
def serve_css(path):
    return send_from_directory('static/css', path)

@app.route('/images/<path:path>')
def serve_images(path):
    return send_from_directory('static/images', path)

# API Calls
@app.route('/api')
def show_hand():
    return jsonify(
        name= config["ludobox_name"],
        version =  __version__,
        env = { "python" :  sys.version },
        config = config
    )

@app.route('/api/<path:path>')
def serve_api(path):
    return send_from_directory('data', path)

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

    # TODO : fix hack to check if info comes from json or straight HTML form
    if len(request.form) != 20:
        info = json.loads(request.form["info"])
    else : # not a JSON
        info = parse_post_form(request.form)

    files = request.files.getlist('files')
    print files

    data_path = write_game(info, files, app.config["DATA_DIR"])

    # try:
    #     # TODO split this in 2 funcs "write json" and "write attachements"
    # except LudoboxError as e:
    #     # TODO replace this dummy return by a true page showing the failed add
    #     return redirect(url_for("static", filename="index.html"))

    # Generate the HTML pages !
    if not generate_all(app.config["DATA_DIR"], OUTPUT_DIR):
        # TODO replace this dummy return by a true page showing the failed gen
        return redirect(url_for("static", filename="index.html"))

    # TODO replace this dummy return by a true page showing the successful add
    return redirect(url_for("static", filename="index.html"))

def parse_post_form(form):
    # An empty dictionnary to store all the data from the form
    data = {
        "type": "game",
        "genres": {"fr": []},
        "title": {"fr": ""},
        "description": {"fr": ""},
        "themes": {"fr": []},
        "publishers": [],
        "publication_year": "",
        "authors": [],
        "illustrators": [],
        "duration": "",
        "audience": [],
        "players_min": 0,
        "players_max": 0,
        "fab_time": 0,
        "requirements": {"fr": []},
        "source": "",
        "license": "",
        "languages": [],
        "ISBN": [],
        "timestamp_add": ""
    }

    # retrieving all the datas
    data['type'] = request.form['type']
    data['genres']['fr'] = \
        [g.strip() for g in request.form['genres'].split(',')]
    data['title']['fr'] = request.form['title']
    data['description']['fr'] = request.form['description'].strip()
    data['themes']['fr'] = \
        [t.strip() for t in request.form['themes'].split(',')]
    data['publishers'] = \
        [p.strip() for p in request.form['publishers'].split(',')]
    data['publication_year'] = int(request.form['publication_year'])
    data['authors'] = \
        [a.strip() for a in request.form['authors'].split(',')]
    data['illustrators'] = \
        [i.strip() for i in request.form['illustrators'].split(',')]
    data['duration'] = int(request.form['duration'])
    if 'gameAudience_children' in request.form:
        data['audience'].append('children')
    if 'gameAudience_teens' in request.form:
        data['audience'].append('teens')
    if 'gameAudience_adults' in request.form:
        data['audience'].append('adults')
    data['players_min'] = int(request.form['players_min'])
    data['players_max'] = int(request.form['players_max'])
    data['fab_time'] = int(request.form['fab_time'])
    data['requirements']['fr'] = \
        [r.strip() for r in request.form['requirements'].split(',')]
    data['source'] = request.form['source']
    data['license'] = request.form['license']
    data['languages'] = \
        [l.strip() for l in request.form['languages'].split(',')]
    data['ISBN'] = \
        [isbn.strip() for isbn in request.form['ISBN'].split(',')]
    data['timestamp_add'] = datetime.now().isoformat()

    return data
