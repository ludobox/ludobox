#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app
from flask_socketio import SocketIO, emit

# socket io
socket = SocketIO()

@socket.on('connect')
def test_connect():
    current_app.logger.debug("socket io connected")
