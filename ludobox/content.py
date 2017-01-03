#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json

from werkzeug import secure_filename
from slugify import slugify
from jsonschema import validate

from ludobox.errors import LudoboxError

from ludobox.config import read_config
config = read_config()

with open(os.path.join(os.getcwd(), "ludobox/model/schema.json")) as f :
    schema = json.load(f)

def validate_game_data(data):
    """Validate game data based on existing data VS a JSON Schema"""
    print validate(data, schema)




# TODO test this function with different scenari: existant/inexistant/not
#   readable dir, info.json present/absent/not readable, with/without attached
#   file
def read_game_info(path):
    """
    Read all the info available about the game stored at the provided path.

    Arguments:
    path -- directory where the game info and data are stored

    Returns a dictionary containing the game data.

    >>> data = read_game_info("tests/functional/data/hackathon/borgia-le-jeu-malsain")
    >>> print(', '.join(data['audience']))
    adults
    >>> print(', '.join(data['authors']))
    René
    >>> print(', '.join(data['themes']['fr']))
    Médiéval, Salopard

    If anythin goes wrong raise a LudoboxError containing description of the
    error and advice for fixing it.

    >>> try:
    ...     data = read_game_info("stupid_path/no_game")
    ... except LudoboxError as e:
    ...     print(e.message)
    <No such file or directory> occured while reading game 'no_game' info file 'stupid_path/no_game/info.json'

    The game data can come from:
    *   the info.json file
    *   the attached files found in the dir
    *   somme are also computed from other data like a cleaned name suitable
        for url generation (slugified name)
    """
    # Load JSON from the description file of the game
    json_path = os.path.join(path, "info.json")
    try:
        with open(json_path, "r") as json_file:
            data = json.load(json_file)
    except IOError as e:
        # TODO Handle more precisely the error and provide an advice for
        #   solving the problem
        # Create a very explicit message to explain the problem
        message = "<{error}> occured while "\
                  "reading game '{game}' info file '{json}'".format(
                    error=e.strerror,
                    game=os.path.basename(path),
                    json=e.filename)
        raise LudoboxError(message)

    # TODO Add some attachment info

    # Add permalink
    data["slug"] = slugify(data["title"]["fr"])

    return data

def write_game_info(data, attachments, data_dir):
    """
    Write a JSON file description of a game according to the provided data and
    attachment files in a dedicated directory named after the game.

    Arguments:
    data -- a dictionnary storing all the information about the game. It
            exactly mimic the structure of the disired JSON file. The
            data["title"]["fr"] must exist, no other verification is made to
            check it contains coherent structure or data.
    attachments -- list of files attached to the game (rules, images...).
    data_dir -- directory where all the game directories are stored i.e. where
                a directory named after the game will be created to store the
                JSON file. It must exist.

    Returns the path to the directory created to store the JSON file (it
    should be named after the game!).

    Raises a LudoboxError if anything goes wrong.

    the :func:`write_game_info()` and :func:`read_game_info()` function should
    work nicely together. Any file writen with the first should be readable by
    the second:

    >>> game_name = "gametest"  # a title with no slugification problem
    >>> data = {
    ...     "type": game_name,
    ...     "genres": {"fr": ["genre 1", "genre 2"]},
    ...     "title": {"fr": "gametest"},
    ...     "description": {"fr": "A very long description"},
    ...     "themes": {"fr": ["theme 1", "theme 2"]},
    ...     "publishers": ["publisher 1", "publisher 2"],
    ...     "publication_year": "1979",
    ...     "authors": ["author 1", "author 2"],
    ...     "illustrators": ["illustrator 1", "illustrator 2"],
    ...     "duration": "120",
    ...     "audience": ["teen", "adults"],
    ...     "players_min": 1,
    ...     "players_max": 10,
    ...     "fab_time": 30,
    ...     "requirements": {"fr": ["printer", "3d printer", "dice"]},
    ...     "source": "http://www.thegame.org/game1",
    ...     "license": "CC0",
    ...     "languages": ["en", "fr", "br"],
    ...     "ISBN": ["1234567890123", "1234567890"],
    ...     "timestamp_add": "10/10/2015 14:52:35"
    ... }
    >>> import tempfile
    >>> data_dir = tempfile.mkdtemp()  # The data directory must exist
    >>> game_dir = write_game_info(data, [],data_dir)
    >>> data2 = read_game_info(game_dir)
    >>> print(data2["title"]["fr"])
    gametest

    If anythin goes wrong raise a LudoboxError containing description of the
    error and advice for fixing it.

    >>> data = {"title": {"fr": "gametest"}}
    >>> try:
    ...     write_game_info(data, [], "stupid/path/to/nowhere")
    ... except LudoboxError as e:
    ...     print(e.message)
    Error occured while writing game info file to path 'stupid/path/to/nowhere'. Data directory 'stupid/path/to/nowhere' does not exist or is not a directory.

    """
    # first we need the slugified name of the game
    try:
        slugified_name = slugify(data["title"]["fr"])
    except KeyError as e:
        # TODO Handle more precisely the error and provide an advice for
        #   solving the problem
        # Create a very explicit message to explain the problem
        message = "KeyError occured while "\
                  "writing game info file to path '{path}'. "\
                  "Impossible to access data['title']['fr'].".format(
                    path=data_dir)
        raise LudoboxError(message)

    # Check if the data directory exists
    if not os.path.exists(data_dir) or not os.path.isdir(data_dir):
        # TODO Handle more precisely the error and provide an advice for
        #   solving the problem
        # Create a very explicit message to explain the problem
        message = "Error occured while "\
                  "writing game info file to path '{path}'. "\
                  "Data directory '{data_dir}' does not "\
                  "exist or is not a directory.".format(
                    path=data_dir,
                    data_dir=data_dir)
        raise LudoboxError(message)

    # Create a directory afte the cleaned name of the game
    game_path = os.path.join(data_dir, slugified_name)
    try:
        os.makedirs(game_path)
    except Exception as e:
        # TODO Handle more precisely the error and provide an advice for
        #   solving the problem
        # Create a very explicit message to explain the problem
        message = "<{error}> occured while "\
                  "writing game info file to path '{path}' for "\
                  "game '{game}'. Impossible to create "\
                  "directory '{game_path}' to store JSON file.".format(
                    error=e.strerror,
                    path=data_dir,
                    game=slugified_name,
                    game_path=os.path.abspath(game_path))
        raise LudoboxError(message)

    # Convert the data to JSON
    try:
        content = json.dumps(data, sort_keys=True, indent=4)
    except IOError as e:
        # Cleanup anything previously created
        # TODO use clean(game=game_name)
        shutil.rmtree(game_path, ignore_errors=True)
        # TODO Handle more precisely the error and provide an advice for
        #   solving the problem
        # Create a very explicit message to explain the problem
        message = "<{error}> occured while "\
                  "writing game info file to path '{path}' for "\
                  "game '{game}'. Impossible to create JSON representation "\
                  "of the provided data.".format(
                    error=e.strerror,
                    path=data_dir,
                    game=slugified_name)
        raise LudoboxError(message)

    # Write the JSON file itself
    json_path = os.path.join(game_path, "info.json")
    try:
        with open(json_path, "w") as json_file:
            json_file.write(content.encode('utf-8'))
    except IOError as e:
        # Cleanup anything previously created
        # TODO use clean(game=game_name)
        shutil.rmtree(game_path, ignore_errors=True)
        # TODO Handle more precisely the error and provide an advice for
        #   solving the problem
        # Create a very explicit message to explain the problem
        message = "<{error}> occured while "\
                  "writing game info file to path '{path}' for "\
                  "game '{game}'. "\
                  "Impossible to write JSON file '{json}'.".format(
                    error=e.strerror,
                    path=data_dir,
                    game=slugified_name,
                    json=json_path)
        raise LudoboxError(message)

    # Write the attached files
    # TODO write actual code here
    # TODO add some tests for this code
    if attachments:
        # Create a directory to store the uploaded files
        attachments_path = os.path.join(game_path, "files")
        try:
            os.makedirs(attachments_path)
        except Exception as e:
            # TODO Handle more precisely the error and provide an advice for
            #   solving the problem
            # Create a very explicit message to explain the problem
            message = "<{error}> occured while "\
                      "writing game info to path '{path}' for "\
                      "game '{game}'. Impossible to create "\
                      "directory '{attachments_path}' to store the attached "\
                      "files.".format(
                        error=e.strerror,
                        path=data_dir,
                        game=slugified_name,
                        attachments_path=os.path.abspath(attachments_path))
            raise LudoboxError(message)

        # Write all the files
        for f in attachments:
            file_clean_name = secure_filename(f.filename)
            file_path = os.path.join(attachments_path, file_clean_name)
            try:
                f.save(file_path)
            except Exception as e:
                # TODO Handle more precisely the error and provide an advice
                #   for solving the problem
                # Create a very explicit message to explain the problem
                message = "<{error}> occured while "\
                          "writing game info to path '{path}' for "\
                          "game '{game}'. Impossible to save file"\
                          "'{file_path}' in the attachment directory "\
                          "'{attachments_path}'.".format(
                            error=e.strerror,
                            path=data_dir,
                            game=slugified_name,
                            file_path=os.path.abspath(file_path),
                            attachments_path=os.path.abspath(attachments_path))
                raise LudoboxError(message)

    return game_path

def build_index():
    """Create an index of all games and content avaible inside the box"""

    # TODO : check are you sure to update index (y/n) ?
    # if os.path.exists(config["index_path"]):

    info_files = []

    # loop through all folders
    for item in os.listdir(config["data_dir"]) :
        path = os.path.join(config["data_dir"],item)
        # get only folders
        if os.path.isdir(path):
            info_file = os.path.join(path, "info.json")
            # check if folder contains a info.json file
            if os.path.exists(info_file):
                with open(info_file, "r") as f:
                    info = json.load(f)
                info_files.append(info)

    # TODO : filter infos to make the index file smaller
    with open(config["index_path"], "wb") as index_file:
        info = json.dump(info_files, index_file)
