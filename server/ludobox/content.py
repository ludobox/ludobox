#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file regoups all operations related to content manipulation (create, update, read, validate, delete)

There are three kinds of content :
- game
- workshop
- page

"""

import os
import json

from flask import current_app
from flask_security import current_user

from ludobox.utils import json_serial # convert datetime

from jsonschema import validate, ValidationError

from ludobox.config import read_config
from ludobox.attachments import write_attachments, get_attachements_list, check_attachments

from ludobox.flat_files import create_resource_folder, write_info_json, delete_resource_folder, read_info_json
from ludobox.errors import LudoboxError
from ludobox.utils import get_resource_slug
from ludobox.history import make_create_event, make_update_event, make_update_state_event, add_event_to_history

config = read_config()

# define contents
VALID_CONTENT_TYPES = ["game", "workshop", "page"]

# load models
schemas = {}
with open(os.path.join(os.getcwd(), "model/game.json")) as game_schema_file :
    schemas["game"] = json.load(game_schema_file)

def get_content_type(data):

    # try to guess the content type
    try :
        content_type = data["content_type"]
    except KeyError:
        message = "<Missing Content Type> You need to explicitely "\
        "define a 'content_type' property to read this content. "\
        "Authorized content types are : {allowed}".format(
            allowed=" ,".join(VALID_CONTENT_TYPES)
            )
        raise LudoboxError(message)

    assert content_type in VALID_CONTENT_TYPES

    # TODO : implement those guys
    if content_type in ["page", "workshop"] :
        raise NotImplementedError("Page and workshop... coming soon !")

    return content_type

def validate_content(data):
    """
    Validate game data VS a JSON Schema

    returns a list of errors or None if valid
    """
    content_type = get_content_type(data)
    errors = validate(data, schemas[content_type])
    return errors

def read_content(path):
    """
    Read all the info available about the game stored at the provided path.

    Arguments:
    path -- directory where the game info and data are stored

    Returns a dictionary containing the game data.

    The game data contains:
    *   the info.json file
    *   a list of attached files found in the '/files' dir
    """

    data = read_info_json(path)

    # validate data and catch errors to flag content
    try :
        validate_content(data)
    except ValidationError as e:
        data["has_errors"] = True
        data["errors"] = [ str(e) ]

    # add files attachments list
    data["files"] = get_attachements_list(path)

    return data

def create_content(info, attachments, data_dir):
    """
    Write a JSON file description of a game according to the provided data and
    attachment files in a dedicated directory named after the game.

    Arguments:
    info -- a dictionnary storing all the information about the content. It
            exactly mimic the structure of the disired JSON file. The
            data["title"] must exist, no other verification is made to
            check it contains coherent structure or data.
    attachments -- list of files attached to the content (images, PDF...). All files will be stored in a '/files' folder
    data_dir -- directory where all the game directories are stored i.e. where
                a directory named after the content will be created to store the
                JSON file. It must exist.

    Returns the path to the directory created after the name of the slugified title of the content.
    """

    # get slug and add name
    slugified_name = get_resource_slug(info)
    info["slug"] = slugified_name

    # if info about files, remove it
    info.pop('files', None)

    # validate game data
    validate_content(info)

    # add default state
    info["state"] = "needs_review"

    # check attachments
    if attachments:
        check_attachments(attachments)

    # Create a directory after the cleaned name of the content
    content_path = os.path.join(data_dir, slugified_name)
    create_resource_folder(content_path)

    # get current user
    user = None
    if current_user.is_authenticated :
        user = current_user.email

    # create event and add to history record
    event = make_create_event(info, user=user)
    info_with_updated_history = add_event_to_history(info, event)

    # create the JSON file
    write_info_json(info_with_updated_history, content_path)

    # Write the attached files
    if attachments:
        write_attachments(attachments, content_path)

    return content_path

def update_content_info(resource_path, new_info, state=None):
    """
    Update game info based on changes

    - create patch changes using JSON patch (RFC 6902)
    - store patch in an history array within the JSON file
    - replace original info content with updated content
    """

    original_info = read_content(resource_path)

    # get current user
    user = None
    if current_user.is_authenticated :
        user = current_user.email

    # create patch
    if state:
        event = make_update_state_event(original_info, state, user=user)
    else :
        event = make_update_event(new_info, original_info, user=user)

    if event is None :
        return original_info

    new_info_with_history = add_event_to_history(original_info, event)

    # write updated game to file
    write_info_json(new_info_with_history, resource_path)
    return new_info_with_history

def get_content_index(short=True):
    """Loop through all and parse an index of available content"""
    info_files = []

    # get an abbreged version of the index
    if short :
        wanted_keys = [
            "title",
            "description",
            "slug",
            "audience",
            "content_type",
            "has_errors"
            ]

    # loop through all folders
    for item in os.listdir(current_app.config["DATA_DIR"]) :
        path = os.path.join(current_app.config["DATA_DIR"],item)

        # get only folders
        if os.path.isdir(path):
            info_file = os.path.join(path, "info.json")

            # check if folder contains a info.json file
            if os.path.exists(info_file):
                info = read_content(path)
                if short :
                    info_files.append({ k : info[k] for k in wanted_keys if k in info.keys() })
                else :
                    info_files.append(info)

    sorted_info_files = sorted(info_files, key=lambda k: k['title'])
    return sorted_info_files

def delete_content(game_path):
    """Remove useless elements from the game folder."""
    delete_resource_folder(game_path)
