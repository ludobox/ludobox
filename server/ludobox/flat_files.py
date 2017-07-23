#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Everything that relates to store/retrieve/update information on flat files system used by ludobox.

The flat file system is as follow :
- a main folder named after a slugified (secure filename) of the title of the content
- a '/files' folder inside the main folder containing all files

So an example of the main structure will be :

    data /
        my-awesome-game-fr /
            info.json
            files/
                myfile1.png
                myfile2.pdf
"""

import os
import json
import shutil

from flask import current_app

from ludobox.errors import LudoboxError
from ludobox.utils import json_serial # convert datetime

def create_resource_folder(resource_folder_path) :
    """Create the dir to store the game"""
    try:
        os.makedirs(resource_folder_path)
    except Exception as e:
        message = "<{error}> occured while writing game info file."\
                  "Impossible to create directory '{resource_folder_path}'.".format(
                    error=e.strerror,
                    resource_folder_path=os.path.abspath(resource_folder_path))
        raise LudoboxError(message)
    current_app.logger.debug("path created : %s"%resource_folder_path)

def delete_resource_folder(resource_folder_path):
    """Delete an existing rep containing data of a game"""
    if os.path.exists(resource_folder_path):
        shutil.rmtree(resource_folder_path, ignore_errors=True)

def write_info_json(info, resource_folder_path):
    """Write a JSON file based on valid resource data"""

    # Convert the data to JSON into file
    content = json.dumps(info, sort_keys=True, indent=4, default=json_serial)
    json_path = os.path.join(resource_folder_path, "info.json")

    try:
        with open(json_path, "w") as json_file:
            json_file.write(content.encode('utf-8'))
    except IOError as e:
        # Cleanup anything previously created
        delete_resource_folder(resource_folder_path)

        # TODO Handle more explicit message
        message = "<{error}> occured while "\
                  "writing game info file to path '{path}'"\
                  "Impossible to write JSON file '{json}'.".format(
                    error=e.strerror,
                    path=resource_folder_path,
                    json=json_path)
        raise LudoboxError(message)

def read_info_json(resource_folder_path):
    """Load JSON from the description file of the game"""

    json_path = os.path.join(resource_folder_path, "info.json")

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
                    game=os.path.basename(resource_folder_path),
                    json=e.filename)
        raise LudoboxError(message)

    return data
