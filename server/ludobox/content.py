#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json

from ludobox.utils import json_serial # convert datetime

from jsonschema import validate, ValidationError

from ludobox.config import read_config
from ludobox.attachments import write_attachments
from ludobox.flat_files import create_resource_folder, write_info_json, delete_resource_folder, read_info_json
from ludobox.errors import LudoboxError
from ludobox.utils import get_resource_slug
from ludobox.history import make_create_event, make_update_event, add_event_to_history

config = read_config()

with open(os.path.join(os.getcwd(), "model/schema.json")) as f :
    schema = json.load(f)

def validate_game_data(data):
    """Validate game data based on existing data VS a JSON Schema"""
    return validate(data, schema)

# TODO test this function with different scenari: existant/inexistant/not readable dir, info.json present/absent/not readable, with/without attached file
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
    data = read_info_json(path)

    # validate data
    validate_game_data(data)

    # TODO Add some attachment info

    # Add permalink
    data["slug"] = get_resource_slug(data)

    return data

def write_game(info, attachments, data_dir):
    """
    Write a JSON file description of a game according to the provided data and
    attachment files in a dedicated directory named after the game.

    Arguments:
    info -- a dictionnary storing all the information about the game. It
            exactly mimic the structure of the disired JSON file. The
            data["title"] must exist, no other verification is made to
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
    """

    slugified_name = get_resource_slug(info)

    # Create a directory after the cleaned name of the game
    game_path = os.path.join(data_dir, slugified_name)
    create_game_path(game_path)

    # create JSON resource
    write_info_json(info, game_path)

    # Write the attached files
    if attachments:
        try :
            write_attachments(attachments, game_path)
        except LudoboxError as e:
            raise LudoboxError(str(e))

    return game_path

def write_game_info(info, game_path):
    """Write a JSON file based on valid resource data"""

    # validate game data
    try:
        validate_game_data(info)
    except ValidationError as e:
        print e
        # Cleanup anything previously created
        clean_game(game_path)
        raise ValidationError(e)

    write_info_json(info, game_path)

def get_games_index():
    """Loop through all and parse an index of available games"""
    info_files = []

    # loop through all folders
    for item in os.listdir(config["data_dir"]) :
        path = os.path.join(config["data_dir"],item)
        # get only folders
        if os.path.isdir(path):
            info_file = os.path.join(path, "info.json")
            # check if folder contains a info.json file
            if os.path.exists(info_file):
                info = read_game_info(path)
                wanted_keys = [
                    "title",
                    "description",
                    "slug",
                    "audience",
                    "content_type"
                    ]

                info_files.append({ k : info[k] for k in wanted_keys if k in info.keys() })

    sorted_info_files = sorted(info_files, key=lambda k: k['title'])
    return sorted_info_files

def update_game_info(game_path, new_game_info):
    """
    Update game info based on changes

    - create patch changes using JSON patch (RFC 6902)
    - store patch in an history array within the JSON file
    - replace info original content with updated content
    """

    original_info = read_game_info(game_path)

    # create patch
    update = history_update(new_game_info,original_info)

    if update is None :
        return original_info

    # write updated game to file
    write_info_json(new_game_info, game_path )
    return new_game_info

def clean_game(game_path):
    """Remove useless elements from the game folder."""
    delete_resource_folder(game_path)
