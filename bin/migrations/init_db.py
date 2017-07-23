#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ludobox import create_app
from ludobox.models import db, Role, create_default_roles

if __name__ == '__main__':
    app=create_app()
    with app.app_context():
        db.create_all()
        create_default_roles()
    print "Tables created."
