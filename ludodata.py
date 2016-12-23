#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import json
import yaml
import requests
import subprocess
from slugify import slugify

# defaults
INDEX_DAT_ID = "1c25ff624b817f828b03915eb83502b3f84b0f2168ec859941254bfb56d091c1"
GAMES_LIST_FILE =os.path.join(os.getcwd(),"games.yml")

def apply_config():
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

def read_index(index_path):
    """Read the JSON index"""
    with open(index_path, "r") as indexfile:
        index = json.load(indexfile)
        game_index = { g["name"] : g["id"] for g in index }
        print "Index loaded : %s games."%len(game_index)
    return game_index

def read_games_list():
    """Read the YAML list of games"""
    with open(GAMES_LIST_FILE, "r") as gamefile:
        game_list = yaml.load(gamefile)
        print "Games list loaded : %s games"%len(game_list["games"])
    return game_list["games"]

def download_with_dat(dat_id, data_dir, dir) :
    """Download a dat rep into data dir"""
    # cmd = 'dat'
    cmd = "dat --exit %s %s"%(dat_id, dir)
    print cmd
    p = subprocess.Popen(cmd, shell=True, cwd=data_dir, stdin=subprocess.PIPE)
    p.wait() # wait until it finishes

def update_with_dat(games_list, config, update_index=False, update_games=False):
    """Main function to launch the update process using Dat"""

    # download the index
    if not os.path.isfile(config["index_path"]) or update_index :
        download_with_dat(INDEX_DAT_ID, config["data_dir"], 'index')

    games_index = read_index(config["index_path"])

    # download games
    if update_games :
        for game_name in games_list["games"]:
            dat_id = games_index[game_name]
            slug = slugify(game_name)
            download_with_dat(dat_id, slug)
        print "Games data updated."

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

def build_url(base_url, dest):
    """A simple URL parser"""
    return base_url + "/api/" + dest

def update_from_web_server(games_list, config, update_index=False, update_games=False):
    """Alternative methods to update through another Ludobox server"""

    if not os.path.isfile(config["index_path"]) or update_index :
        # update index
        url = build_url(config["web_server_url"], "index/index.json")
        download_from_server(url, config["data_dir"], "index")

    # download games
    if update_games:
        for game_name in games_list:
            slug = slugify(game_name)
            url = build_url(config["web_server_url"], slug+"/info.json")
            download_from_server(url, config["data_dir"], slug)
        print "Games data updated."

def update_data(config, update_index=False, update_games=False):

    games_list = read_games_list()
    data_dir = config["data_dir"]
    base_url = config["web_server_url"]

    if config["update_mode"] == "dat":
        update_with_dat(games_list, config, update_index=update_index, update_games=update_index)
    elif config["update_mode"] == "web":
        update_from_web_server(games_list, config, update_index=update_index, update_games=update_index)

if __name__ == "__main__":

    # Read config
    config = apply_config()
    print config

    # update data using appropriate config
    update_data(config, update_index=True, update_games=True)
