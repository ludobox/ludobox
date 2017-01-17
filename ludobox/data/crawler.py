#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import requests
from slugify import slugify

from ludobox.config import read_config

# read and parse config
config = read_config()

def build_url(dest):
    """A simple URL parser"""
    if dest is None :
        return config["web_server_url"] + "/api"
    else :
        return config["web_server_url"] + "/api/" + dest

def get_data_from_api(dest):
    url = build_url(dest)
    r = requests.get(url)
    if r.status_code == 200:
        if "json" in r.headers['content-type']:
            return r.json()
    # TODO : handle API errors / etc

def handshake() :
    """Shake hands with a remote server and get its name"""
    return get_data_from_api(None)

def download_index():
    """Shake hands with a remote server and get its name"""
    return get_data_from_api("index.json")

def download_from_server(url, data_dir, dir) :
    """Download a rep from a ludobox server into data dir"""
    if dir == "index" :
        index_dir = os.path.join(data_dir,'index')
        if not os.path.exists(index_dir):
            os.makedirs(index_dir)
        json_file_name = os.path.join(index_dir,'index.json')
    else :
        game_dir = os.path.join(data_dir,dir)
        if not os.path.exists(game_dir):
            os.makedirs(game_dir)
        json_file_name = os.path.join(game_dir, "info.json")

    r = requests.get(url)
    if r.status_code == 200:
        if "json" in r.headers['content-type']:
            with open(json_file_name, 'w') as f :
                json.dump(r.json(), f)
            print "Data from %s saved in %s "%(url,json_file_name)
    else :
        # TODO: raise ValueError("Wrong :%s"%r.headers)
        return {}

def update_from_web_server(games_list, config, update_index=False, update_games=False):
    """Alternative methods to update through another Ludobox server"""

    if not os.path.isfile(config["index_path"]) or update_index :
        # update index
        url = build_url("index/index.json")
        download_from_server(url, config["data_dir"], "index")

    # download games
    if update_games:
        for game_name in games_list:
            slug = slugify(game_name)
            url = build_url(slug+"/info.json")
            download_from_server(url, config["data_dir"], slug)
        print "Games data updated."

def download_game_from_remote_server(slug) :

    info_url = build_url(slug+"/info.json")

    # download JSON file
    download_from_server(info_url, config["data_dir"], slug)

    # download attachements
    # download_from_server()
