#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import requests

from ludobox.config import read_config, read_games_list
from ludobox.dat import update_with_dat
from ludobox.crawler import update_from_web_server

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
    config = read_config()
    print config

    # update data using appropriate config
    update_data(config, update_index=True, update_games=True)
