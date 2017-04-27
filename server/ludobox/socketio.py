#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_socketio import SocketIO, emit

# socket io
socket = SocketIO()

@socket.on('connect')
def test_connect():
    print  "socket io connected"

def notify_download_end():
    """Notify client that the download ended"""
    emit("downloadEnded", {"url" : url, "filename" : filename }, namespace='/')
