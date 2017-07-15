#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ludobox.models import db, Role
from ludobox import create_app

def create_default_roles():
    # create default roles
    user_role = Role(name='contributor')
    editor_role = Role(name='editor')
    super_user_role = Role(name='superuser')
    db.session.add(user_role)
    db.session.add(editor_role)
    db.session.add(super_user_role)
    db.session.commit()

if __name__ == '__main__':
    app=create_app()
    with app.app_context():
        db.create_all()
        create_default_roles()
    print "Tables created."
