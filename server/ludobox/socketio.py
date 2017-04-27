#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_socketio import SocketIO, emit

# socket io
socket = SocketIO()

@socket.on('connect')
def test_connect():
    print  "socket io connected"
