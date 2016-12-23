#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import json
import yaml
import requests
import subprocess
from slugify import slugify

# data rep
data_path=os.path.join(os.getcwd(),"data")
if not os.path.exists(data_path):
    os.makedirs(data_path)
print "Data will be stored at : %s"%data_path

# index
index_dat_id = "1c25ff624b817f828b03915eb83502b3f84b0f2168ec859941254bfb56d091c1"
index_dir = os.path.join(data_path, 'index')
index_path = os.path.join(index_dir, 'index.json')

# games_list
games_list_file =os.path.join(os.getcwd(),"games.yml")

def read_index():
    """Read the JSON index"""
    with open(index_path, "r") as indexfile:
        index = json.load(indexfile)
        game_index = { g["name"] : g["id"] for g in index }
        print "Index loaded : %s games."%len(game_index)
    return game_index

def read_games_list():
    """Read the YAML list of games"""
    with open(games_list_file, "r") as gamefile:
        game_list = yaml.load(gamefile)
        print "Games list loaded : %s games"%len(game_list["games"])
    return game_list["games"]

def download_with_dat(dat_id, dir) :
    """Download a dat rep into data dir"""
    # cmd = 'dat'
    cmd = "dat --exit %s %s"%(dat_id, dir)
    print cmd
    p = subprocess.Popen(cmd, shell=True, cwd=data_path, stdin=subprocess.PIPE)
    p.wait() # wait until it finishes

def update_with_dat(games_index, games_list, index_to_update=False, games_to_update=False):
    """Main function to launch the update process using Dat"""

    # download the index
    if not os.path.isfile(index_path) or index_to_update :
        download_with_dat(index_dat_id, 'index')

    # download games
    if games_to_update :
        for game_name in games_list["games"]:
            dat_id = games_index[game_name]
            slug = slugify(game_name)
            download_with_dat(dat_id, slug)
        print "Games data updated."

def download_from_server(url, dir) :
    """Download a rep from a ludobox server into data dir"""
    if dir == "index" :
        if not os.path.exists(index_dir):
            os.makedirs(index_dir)
        json_file_name = index_path
    else :
        game_dir = os.path.join(data_path,dir)
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
    return base_url + "/api/" + dest

def update_from_server(base_url, games_index, games_list):
    """Alternative methods to update through another Ludobox server"""
    # print url, games_index, games_list

    # update index
    url = build_url(base_url, "index/index.json")
    download_from_server(url, "index")

    # download games
    for game_name in games_list:
        slug = slugify(game_name)
        url = build_url(base_url, slug+"/info.json")
        download_from_server(url, slug)

if __name__ == "__main__":

    # parse files
    games_index = read_index()
    games_list = read_games_list()

    # update_with_dat(games_index, games_list)
    update_from_server("http://localhost:8080", games_index, games_list)
