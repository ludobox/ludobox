#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import urllib
import requests
from flask import current_app
from flask_socketio import emit

from ludobox.config import read_config
from ludobox.socketio import socket

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

def download_from_server(url, dest_dir, filename) :
    """Download a rep from a ludobox server into data dir"""

    file_path = os.path.join(dest_dir, filename)

    # direct download
    testfile = urllib.URLopener()
    testfile.retrieve(url, file_path)

    current_app.logger.debug("Data from %s saved in %s "%(url,filename))

    socket.emit("downloadEnded", {"url" : url, "filename" : filename }, namespace='/')
