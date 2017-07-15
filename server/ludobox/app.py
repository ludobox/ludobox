#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ludobox import create_app
from ludobox.routes.static import statics
from ludobox.routes.api import rest_api
from ludobox.socketio import socket
from ludobox.security import security
from ludobox.admin import admin

# create a web server instance
app = create_app()

# add socketIO support
socket.init_app(app)

# register routes
app.register_blueprint(statics)
app.register_blueprint(rest_api)

# define a context processor for merging flask-admin's template context into the flask-security views.
# @security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )
