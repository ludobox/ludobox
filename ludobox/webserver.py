#!/usr/bin/env python
# -*- coding: utf-8 -*-

import flask
from ludobox.config import read_config
from ludobox.content import write_game_info

# parse config
config = read_config()

app = flask.Flask("LUDOSERVER")  # web server instance used to defines routes

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
    return flask.redirect(flask.url_for("static", filename="index.html"))

@app.route('/api/<path:path>')
def serve_api(path):
    return flask.send_from_directory('data', path)

@app.route('/api/handshake')
def show_hand():
    return flask.jsonify( name= config["ludobox_name"] )

@app.route('/addgame', methods=["POST"])
def serve_addgame():
    """Process the uploads of new games."""

    if config["upload_allowed"] is False:
        return flask.redirect(flask.url_for("static", filename="index.html"))

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
    data['type'] = flask.request.form['type']
    data['genres']['fr'] = \
        [g.strip() for g in flask.request.form['genres'].split(',')]
    data['title']['fr'] = flask.request.form['title']
    data['description']['fr'] = flask.request.form['description'].strip()
    data['themes']['fr'] = \
        [t.strip() for t in flask.request.form['themes'].split(',')]
    data['publishers'] = \
        [p.strip() for p in flask.request.form['publishers'].split(',')]
    data['publication_year'] = int(flask.request.form['publication_year'])
    data['authors'] = \
        [a.strip() for a in flask.request.form['authors'].split(',')]
    data['illustrators'] = \
        [i.strip() for i in flask.request.form['illustrators'].split(',')]
    data['duration'] = int(flask.request.form['duration'])
    if 'gameAudience_children' in flask.request.form:
        data['audience'].append('children')
    if 'gameAudience_teens' in flask.request.form:
        data['audience'].append('teens')
    if 'gameAudience_adults' in flask.request.form:
        data['audience'].append('adults')
    data['players_min'] = int(flask.request.form['players_min'])
    data['players_max'] = int(flask.request.form['players_max'])
    data['fab_time'] = int(flask.request.form['fab_time'])
    data['requirements']['fr'] = \
        [r.strip() for r in flask.request.form['requirements'].split(',')]
    data['source'] = flask.request.form['source']
    data['license'] = flask.request.form['license']
    data['languages'] = \
        [l.strip() for l in flask.request.form['languages'].split(',')]
    data['ISBN'] = \
        [isbn.strip() for isbn in flask.request.form['ISBN'].split(',')]
    data['timestamp_add'] = datetime.now().isoformat()

    # We get all the files uploaded
    files = flask.request.files.getlist('files')
    print("UPLOADED FILES:", [f.filename for f in files])

    # Save the game description as pure JSON file
    try:
        # TODO split this in 2 funcs "write json" and "write attachements"
        data_path = write_game_info(data, files, INPUT_DIR)
    except LudoboxError as e:
        # TODO replace this dummy return by a true page showing the failed add
        return flask.redirect(flask.url_for("static", filename="index.html"))

    # Generate the HTML pages !
    if not clean(OUTPUT_DIR):
        # TODO replace this dummy return by a true page showing the failed gen
        return flask.redirect(flask.url_for("static", filename="index.html"))

    if not generate_all(INPUT_DIR, OUTPUT_DIR):
        # TODO replace this dummy return by a true page showing the failed gen
        return flask.redirect(flask.url_for("static", filename="index.html"))

    # TODO replace this dummy return by a true page showing the successful add
    return flask.redirect(flask.url_for("static", filename="index.html"))
