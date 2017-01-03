#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json

from ludobox.config import read_config
config = read_config()

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
