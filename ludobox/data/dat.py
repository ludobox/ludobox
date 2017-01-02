#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess

from ludobox.config import read_config, read_games_list

INDEX_DAT_ID = "1c25ff624b817f828b03915eb83502b3f84b0f2168ec859941254bfb56d091c1"

def read_index(index_path):
    """Read the JSON index"""
    with open(index_path, "r") as indexfile:
        index = json.load(indexfile)
        game_index = { g["name"] : g["id"] for g in index }
        print "Index loaded : %s games."%len(game_index)
    return game_index
    
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
