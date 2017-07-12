#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webserver import app
from models import User

# config
app.config.update(
    DEBUG = True,
    SECRET_KEY = 'secret_xxx'
)
