#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request, abort, jsonify
from flask_security import current_user

from ludobox.security import user_datastore
from ludobox.user import get_latest_changes

# JSON API blueprint
users_api = Blueprint('users', __name__)

@users_api.route('/api/profile', methods=['GET'])
def get_current_user_profile():
    if current_user.is_authenticated:
        user = current_user.to_json()
        user["recent_changes"]  = get_latest_changes(user=user["email"])
        return jsonify(user)
    else :
        abort(403)

@users_api.route('/api/profile/<int:user_id>', methods=['GET'])
def get_user_profile(user_id):
    user = user_datastore.get_user(user_id)
    if user is None:
        return abort(404)
    else :
        user = current_user.to_json()
        user["recent_changes"]  = get_latest_changes(user=user["email"])
        return jsonify(user)

@users_api.route('/api/recent_changes', methods=['GET'])
def get_recent_changes():

    # get user email
    user_id = request.args.get('user_id')
    user_email = None
    user = user_datastore.get_user(user_id)
    print user
    if user is not None :
        user_email = user.to_json()["email"]

    # get time
    before_time = request.args.get('before_time')
    if before_time:
        before_time = int(before_time)

    recent_changes  = get_latest_changes(user=user_email, before_time=before_time)

    return jsonify(recent_changes)
