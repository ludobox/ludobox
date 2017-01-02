#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import yaml
from slugify import slugify

# defaults
GAMES_LIST_FILE =os.path.join(os.getcwd(),"games.yml")

def read_config():
    """Validate and apply settings as defined in config file"""

    # default
    data_dir = os.path.join(os.getcwd(),"data")
    update_mode = "web"
    web_server_url = "http://localhost:8080"

    # Read the YAML config file
    config_path = os.path.join(os.getcwd(),"config.yml")
    with open(config_path, "r") as config_file:
        config = yaml.load(config_file)
        print "Config loaded from %s."%config_path

    # TODO: validate config items and check for unknown params
    if "data_dir" in config.keys() :
        data_dir = config["data_dir"]

    # make data dir
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    print "Data will be stored at : %s"%data_dir

    if "update_mode" in config.keys() :
        update_mode = config["update_mode"]

    if update_mode == "web" and "web_server_url" in config.keys():
        web_server_url = config["web_server_url"]

    index_dir = os.path.join(data_dir, 'index')
    index_path = os.path.join(index_dir, 'index.json')

    return {
        "data_dir" : data_dir,
        "update_mode" : update_mode,
        "web_server_url" : web_server_url,
        "index_dir" : index_dir,
        "index_path" : index_path
    }

def read_games_list():
    """Read the YAML list of games"""
    with open(GAMES_LIST_FILE, "r") as gamefile:
        game_list = yaml.load(gamefile)
        print "Games list loaded : %s games"%len(game_list["games"])
    return game_list["games"]
