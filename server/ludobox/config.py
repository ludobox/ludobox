#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import yaml

import logging
from ludobox.utils import validate_url

logger = logging.getLogger()

def read_config(config_path=os.path.join(os.getcwd(),"config.yml"), *args, **kwargs):
    """Validate and apply settings as defined in config file"""

    # default values
    data_dir = os.path.join(os.getcwd(),"data")
    web_server_url = "http://box.ludobox.net"
    upload_allowed = True
    database_uri = "sqlite:////tmp/ludobox.db"

    logger.info("Loading config from : %s"%config_path)

    # Read the YAML config file
    with open(config_path, "r") as config_file:
        config = yaml.load(config_file)
        # print "Config loaded from %s."%config_path

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

    if "web_server_url" in config.keys():
        web_server_url = config["web_server_url"]

    if "database_uri" in config.keys():
        database_uri = config["database_uri"]

    index_path = os.path.join(data_dir, 'index.json')

    ok_config = {
            "data_dir" : data_dir,
            "web_server_url" : web_server_url,
            "index_path" : index_path,
            "port" : port,
            "ludobox_name" : ludobox_name,
            "upload_allowed" : upload_allowed,
            "database_uri" : database_uri
        }

    logger.info("Config : %s"%ok_config)
    return validate_config(ok_config)

def validate_config(config):
    """Validate config items and check for unknown value or params"""

    assert type(config["port"]) is int
    assert type(config["ludobox_name"]) is str
    if config["web_server_url"] is not None:
        assert validate_url(config["web_server_url"]) is True

    assert type(config["upload_allowed"]) is bool

    # validate data dir
    if not os.path.exists(config["data_dir"]):
        raise ValueError("The path '%s' does not exist. Please create it before starting your Ludobox."%config["data_dir"])
    # print "Data will be stored at : %s"%config["data_dir"]

    return config
