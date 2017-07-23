#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pkg_resources import get_distribution

__version__ = get_distribution('ludobox').version

import os
import sys

import logging
from logging.handlers import RotatingFileHandler

from flask import Flask

from ludobox.config import read_config
from ludobox.models import db
from ludobox.security import security, user_datastore
from ludobox.admin import admin, security_context_processor

DEFAULT_CONFIG_PATH = os.path.join(os.getcwd(),"config.yml")


def create_app(debug=False, config_path=DEFAULT_CONFIG_PATH):
    """Create the Flask application with proper options"""

    config = read_config(config_path=config_path)
    tmpl_dir = os.path.join(os.path.join(os.getcwd(), 'server'), 'templates')

    app = Flask(config["ludobox_name"], template_folder=tmpl_dir)

    app.logger.debug(config_path)
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
    app.config["UPLOAD_ALLOWED"] = config["upload_allowed"] # used for testing

    # setup DB
    db.init_app(app)

    # users rights etc
    # security.init_app(app, datastore=user_datastore)
    # fix from https://github.com/mattupstate/flask-security/issues/340
    security._state = security.init_app(app, user_datastore)
    security.context_processor(security_context_processor)
    app.config["SECURITY_SEND_REGISTER_EMAIL"] = False

    # add admin dashboard
    admin.init_app(app)

    # logs
    formatter = logging.Formatter(
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    logfile = RotatingFileHandler('ludobox.log', maxBytes=100000, backupCount=5)
    logfile.setLevel(logging.DEBUG)
    logfile.setFormatter(formatter)
    app.logger.addHandler(logfile)

    formatter = logging.Formatter('%(levelname)s :: %(message)s')
    terminal = logging.StreamHandler(sys.stdout)
    terminal.setFormatter(formatter)
    app.logger.addHandler(terminal)

    return app
