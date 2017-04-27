#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ludobox.webserver import app
from ludobox.config import read_config
from ludobox.socketio import socket

# parse config
config = read_config()

def get_server_port(port):
    # check if port number is ok
    if port is None : _port = config["port"]
    else : _port = int(port)
    return _port

def serve(debug, port, **kwargs):
    """
    Launch an tiny web server to make the ludobox site available.

    Keyword arguments:
    debug -- bool to activate the debug mode of the Flask server (for
             development only NEVER use it in production).

    kwargs is used here since this function is called by :func:`main` via
    :mod:`argparse`. And all the params are provided automagically by
    :func:`argparse.ArgumentParser.parse_args` converted to a dict using
    :func:`vars`.
    See `Namespace object<https://docs.python.org/2/library/argparse.html#the-namespace-object>`_
    """

    _port = get_server_port(port)
    socket.init_app(app)
    socket.run(app, host='0.0.0.0', port=_port, debug=debug)
