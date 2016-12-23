#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import json
import yaml
import subprocess
from slugify import slugify

# data rep
data_path=os.path.join(os.getcwd(),"data")
if not os.path.exists(data_path):
    os.makedirs(data_path)
print "Data will be stored at : %s"%data_path

# index
index_dat_id = "1c25ff624b817f828b03915eb83502b3f84b0f2168ec859941254bfb56d091c1"
index_path = os.path.join(os.path.join(data_path, 'index'), 'index.json')

# games_list
games_list_file =os.path.join(os.getcwd(),"games.yml")

def download_dat(dat_id, dir) :
    """Download a dat rep into data dir"""
    # cmd = 'dat'
    cmd = "dat --exit %s %s"%(dat_id, dir)
    print cmd
    p = subprocess.Popen(cmd, shell=True, cwd=data_path, stdin=subprocess.PIPE)
    p.wait() # wait until it finishes

def update_index():
    """Download and store the index file"""
    download_dat(index_dat_id, 'index')

def main():
    # options
    index_to_update = False
    games_to_update = False

    # download the index
    if not os.path.isfile(index_path) or index_to_update :
        update_index()

    # read the index
    with open(index_path, "r") as indexfile:
        index = json.load(indexfile)
        game_index = { g["name"] : g["id"] for g in index }
        print "Index loaded : %s games."%len(game_index)

    # read the list of games
    with open(games_list_file, "r") as gamefile:
        game_list = yaml.load(gamefile)
        print "Games list loaded : %s games"%len(game_list["games"])

    # download games
    if games_to_update :
        for game_name in game_list["games"]:
            dat_id = game_index[game_name]
            slug = slugify(game_name)
            download_dat(dat_id, slug)
        print "Games data updated."

if __name__ == "__main__":
    main()
