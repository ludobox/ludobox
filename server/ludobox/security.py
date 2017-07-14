#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_security import Security, SQLAlchemyUserDatastore
from ludobox.models import db, User, Role

# Setup users for Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

security = Security(datastore=user_datastore)
