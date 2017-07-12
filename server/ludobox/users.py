#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webserver import app

from models import User, db, bcrypt

from flask import Flask, Response, redirect, url_for, request, session, render_template, flash
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user



# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# config
app.config.update(
    DEBUG = True,
    SECRET_KEY = 'secret_xxx'
)

@app.route('/register' , methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    user = User(request.form['username'] , request.form['password'],request.form['email'])
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('login'))

@app.route('/login',methods=['GET','POST'])
def login():
    """For GET requests, display the login form. For POSTS, login the current user by processing the form."""
    if request.method == 'GET':
        return render_template('login.html')
    print db

    username = request.form['username']
    password = request.form['password']
    remember_me = False
    if 'remember_me' in request.form:
        remember_me = True

    # validate user & password
    user = User.query.filter_by(username=username).first_or_404()

    if user.is_correct_password(password):
        # do the actual login
        login_user(user, remember = remember_me)
    else:
        flash('Username or Password is invalid' , 'error')
        return redirect(url_for('login'))

    flash('Logged in successfully')
    return redirect(url_for('test'))

@app.route('/test',methods=['GET'])
@login_required
def test() :
    return Response('<p>Test</p>')

# some protected url
@app.route('/')
@login_required
def home():
    return Response("Hello World!")

# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return Response('<p>Logged out</p>')

# # handle login failed
# @app.errorhandler(401)
# def page_not_found(e):
#     return Response('<p>Login failed</p>')

# callback to reload the user object
@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (id) user to retrieve
    """
    print user_id
    return User.query.get(user_id)
