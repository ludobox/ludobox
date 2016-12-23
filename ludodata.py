#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import json
import yaml
import subprocess
from slugify import slugify

# data rep
data_path=os.path.join(os.getcwd(),"data")
print data_path

# index
index_dat_id = "1c25ff624b817f828b03915eb83502b3f84b0f2168ec859941254bfb56d091c1"
index_path = os.path.join(os.path.join(data_path, 'index'), 'index.json')

# games_list
games_list_file =os.path.join(os.getcwd(),"games.yml")

def download_dat(dat_id, dir) :
    """download a dat rep into data dir"""
    # cmd = 'dat'
    cmd = "dat %s %s --exit"%(dat_id, dir)
    print cmd

    p = subprocess.call(cmd, shell=True, cwd=data_path)
    p.wait() # wait until it finishes

if __name__ == "__main__":

    # options
    update_index = False
    update_games = True

    # download the index
    if not os.path.isfile(index_path) or update_index :
        download_dat(index_dat_id, 'index')

    # read the index
    with open(index_path, "r") as indexfile:
        index = json.load(indexfile)
        game_index = { g["name"] : g["id"] for g in index }
        print "index loaded."

    # print index
    with open(games_list_file, "r") as gamefile:
        game_list = yaml.load(gamefile)
        print "games list loaded."

    # download games
    if update_games :
        for game_name in game_list["games"]:
            dat_id = game_index[game_name]
            slug = slugify(game_name)
            download_dat(dat_id, slug)
