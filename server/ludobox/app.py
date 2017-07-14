#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from ludobox.config import read_config

# parse config
config = read_config()
db = SQLAlchemy()

# TODO : move to config
DB_URI = 'sqlite:////tmp/test.db'

def create_app(debug=False):
    """Create the Flask application with proper options"""

    tmpl_dir = os.path.join(os.path.join(os.getcwd(), 'server'), 'templates')

    app = Flask(config["ludobox_name"], template_folder=tmpl_dir)

    # db options
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # security
    app.config['SECURITY_REGISTERABLE'] = True
    app.config['SECURITY_PASSWORD_SALT'] = "dsdskjdksjdksjd&é"

    # setup DB
    db.init_app(app)

    # data options (used for testing)
    app.config["DATA_DIR"] = config["data_dir"]
    print "Data will be stored at %s"%app.config["DATA_DIR"]

    app.config["UPLOAD_ALLOWED"] = config["upload_allowed"] # used for testing
    print "Upload allowed : %s"%app.config["UPLOAD_ALLOWED"]

    app.debug=debug

    return app
