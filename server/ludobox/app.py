#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ludobox import create_app
from ludobox.socketio import socket
from ludobox.security import security
from ludobox.admin import admin
from ludobox.models import db, create_default_roles

from ludobox.routes.static import statics
from ludobox.routes.api import rest_api
from ludobox.routes.games import games_api
from ludobox.routes.users import users_api
from ludobox.routes.files import files_api

# create a web server instance
app = create_app()

# add socketIO support
socket.init_app(app)

# register routes
app.register_blueprint(statics)
app.register_blueprint(rest_api)
app.register_blueprint(users_api)
app.register_blueprint(games_api)
app.register_blueprint(files_api)


@app.before_first_request
def handle_start():
    """Everything that needs a proper init goes there"""

    db.create_all()
    tables = [t.name for t in db.metadata.sorted_tables]
    if "role" not in tables :
        create_default_roles()
