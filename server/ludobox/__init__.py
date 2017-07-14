#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pkg_resources import get_distribution

__version__ = get_distribution('ludobox').version

import os
import logging

from flask import Flask

from ludobox.config import read_config
from ludobox.models import db
from ludobox.security import security, user_datastore
# from ludobox.admin import admin


DEFAULT_CONFIG_PATH = os.path.join(os.getcwd(),"config.yml")


# logs
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)

def create_app(debug=False, config_path=DEFAULT_CONFIG_PATH):
    """Create the Flask application with proper options"""

    config = read_config(config_path=config_path)

    tmpl_dir = os.path.join(os.path.join(os.getcwd(), 'server'), 'templates')

    app = Flask(config["ludobox_name"], template_folder=tmpl_dir)

    # db options
    app.config['SQLALCHEMY_DATABASE_URI'] = config["database_uri"]
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # security
    # TODO : move options to config file
    app.config['SECURITY_REGISTERABLE'] = True
    app.config['SECURITY_PASSWORD_SALT'] = "dsdskjdksjdksjd&é"
    app.config['SECRET_KEY'] = 'secret_xxx'

    # data options (used for testing)
    app.config["DATA_DIR"] = config["data_dir"]
    print "Data will be stored at %s"%app.config["DATA_DIR"]

    app.config["UPLOAD_ALLOWED"] = config["upload_allowed"] # used for testing
    print "Upload allowed : %s"%app.config["UPLOAD_ALLOWED"]

    # setup DB
    db.init_app(app)

    # users rights etc
    security.init_app(app, datastore=user_datastore)
    app.config["SECURITY_SEND_REGISTER_EMAIL"] = False

    # add admin dashboard
    # admin.init_app(app)

    app.debug=debug

    return app
