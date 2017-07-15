#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ludobox.models import db, Role, create_default_roles
from ludobox import create_app

if __name__ == '__main__':
    app=create_app()
    with app.app_context():
        db.create_all()
        create_default_roles()
    print "Tables created."
