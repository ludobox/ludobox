#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app
from flask_security import Security, SQLAlchemyUserDatastore, user_registered
from flask_security.signals import user_registered
from ludobox.models import db, User, Role

# Setup users for Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(datastore=user_datastore)

# add a role on connection
def user_registered_sighandler(app, user, confirm_token):

    # for new user on a fresh install, set superuser rights
    if user.id == 1:
        superuser_role = user_datastore.find_role("superuser")
        user_datastore.add_role_to_user(user, superuser_role)
        db.session.commit()

    # everyone logged in should be recognized as a contributor
    default_role = user_datastore.find_role("contributor")
    user_datastore.add_role_to_user(user, default_role)
    db.session.commit()

user_registered.connect(user_registered_sighandler)
