#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import yaml
from slugify import slugify

from ludobox.utils import validate_url

# defaults
GAMES_LIST_FILE =os.path.join(os.getcwd(),"games.yml")

def read_config(config_path=os.path.join(os.getcwd(),"config.yml")):
    """Validate and apply settings as defined in config file"""

    # default
    data_dir = os.path.join(os.getcwd(),"data")
    update_mode = "web"
    web_server_url = "http://localhost:8080"
    upload_allowed = True

    # Read the YAML config file
    with open(config_path, "r") as config_file:
        config = yaml.load(config_file)
        print "Config loaded from %s."%config_path

    # parse port
    try :
        port = config["port"]
    except KeyError:
        port = 8080 # default value

    # parse name
    try :
        ludobox_name = config["ludobox_name"]
    except KeyError:
        ludobox_name = "My LudoBox" # default value

    if "upload_allowed" in config.keys() :
        upload_allowed = config["upload_allowed"]

    if "data_dir" in config.keys() :
        data_dir = os.path.abspath(config["data_dir"])

    if "update_mode" in config.keys() :
        update_mode = config["update_mode"]

    if update_mode == "web" and "web_server_url" in config.keys():
        web_server_url = config["web_server_url"]

    index_path = os.path.join(data_dir, 'index.json')

    return validate_config(
        {
            "data_dir" : data_dir,
            "update_mode" : update_mode,
            "web_server_url" : web_server_url,
            "index_path" : index_path,
            "port" : port,
            "ludobox_name" : ludobox_name,
            "upload_allowed" : upload_allowed
        }
    )

def validate_config(config):
    """Validate config items and check for unknown value or params"""

    assert type(config["port"]) is int
    assert type(config["ludobox_name"]) is str
    assert validate_url(config["web_server_url"]) is True

    assert type(config["upload_allowed"]) is bool

    # validate data dir
    if not os.path.exists(config["data_dir"]):
        raise ValueError("The path '%s' does not exist. Please create it before starting your Ludobox."%config["data_dir"])
    print "Data will be stored at : %s"%config["data_dir"]

    # assert update modes
    assert config["update_mode"] in ["web", "dat"]
    if config["update_mode"] == "web" :
        assert validate_url(config["web_server_url"]) is True

    return config

def read_games_list():
    """Read the YAML list of games"""
    with open(GAMES_LIST_FILE, "r") as gamefile:
        game_list = yaml.load(gamefile)
        print "Games list loaded : %s games"%len(game_list["games"])
    return game_list["games"]
