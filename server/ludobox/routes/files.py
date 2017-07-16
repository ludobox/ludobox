#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json

from flask import Blueprint, abort, jsonify, request, current_app

from ludobox.attachments import store_files, delete_file, get_attachements_list

# JSON API blueprint
files_api = Blueprint('files', __name__)

@files_api.route('/api/files/<path:path>', methods=["GET"])
def api_serve_files_list(path):
    file_list = get_attachements_list(path)
    return jsonify(file_list)

# @files_api_login_required
@files_api.route('/api/files', methods=["POST"])
def api_post_files():
    """
    This function allow to post 2 things :

    * files : an array of files
    * slug : path/slug of the game

    """

    files = request.files.getlist('files')
    # print("UPLOADED FILES:", [f.filename for f in files])

    game_slug = json.loads(request.form["slug"])
    content_path = os.path.join(current_app.config["DATA_DIR"], game_slug)

    store_files(content_path, files)

    file_list =get_attachements_list(content_path)
    return jsonify({
        "message" : "Success : %s files added."%len(files),
        "files" : file_list
        }), 201

# @files_api_login_required
@files_api.route('/api/files/<string:slug>/<path:path>', methods=["DELETE"])
def api_delete_files(slug,path):

    content_path = os.path.join(current_app.config["DATA_DIR"], slug)
    files_path = os.path.join(content_path, "files")
    to_delete_path = os.path.join(files_path, path)
    print to_delete_path

    # make sure the file actually exists
    if not os.path.isfile(to_delete_path):
        abort(404)

    delete_file(to_delete_path)

    file_list = get_attachements_list(content_path)

    return jsonify(
    {
        "message" : "Success : file %s deleted"%path,
        "files" : file_list
    }), 203
