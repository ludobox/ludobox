#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from flask_security import UserMixin, RoleMixin
from flask_sqlalchemy import SQLAlchemy

# init db
db = SQLAlchemy()

# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name

class User(db.Model, UserMixin):
    """An admin user capable of viewing reports.

    :param str email: email address of user
    :param str password: encrypted password for the user

    """
    __tablename__ = 'user'

    id = db.Column(db.Integer , primary_key=True)
    username = db.Column('username', db.String(20), unique=True , index=True)
    password = db.Column('password' , db.String(255))
    email = db.Column('email',db.String(50),unique=True , index=True)

    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())

    registered_on = db.Column('registered_on' , db.DateTime())

    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return "<User : %s>"%self.email

    def to_json(self):
       return {
        c.name: getattr(self, c.name)
            for c in self.__table__.columns
            if c.name != "password" # avoid showing password :)
        }

def create_default_roles():
    """
    Function to name default roles
    - called during db init by external script './bin/migrations/init_db.py'
    """
    user_role = Role(name='contributor')
    editor_role = Role(name='editor')
    super_user_role = Role(name='superuser')
    db.session.add(user_role)
    db.session.add(editor_role)
    db.session.add(super_user_role)
    db.session.commit()
