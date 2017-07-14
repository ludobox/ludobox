#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ludobox import create_app
from ludobox.routes.static import statics
from ludobox.routes.api import rest_api
from ludobox.socketio import socket

# create a web server instance
app = create_app()

# add socketIO support
socket.init_app(app)

# register routes
app.register_blueprint(statics)
app.register_blueprint(rest_api)
