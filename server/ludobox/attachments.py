#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Manipulate attachement files in the ludobox
"""

import os
from flask import current_app
from werkzeug import secure_filename

from ludobox.errors import LudoboxError

ALLOWED_EXTENSIONS = ["txt", "png", "jpg", "gif", "stl", "zip", "pdf"]

# check if extension is allowed
def allowed_extension(filename):
    """Check for valid file extensions"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# TODO: improve security check for files !
def check_attachments(attachments):
    """Make sure we can upload only safe files"""
    for f in attachments:
        if not allowed_extension(f.filename):
            message = "<{error}> occured while "\
                      "writing. Impossible to save file"\
                      "'{file_clean_name}' because exstension is not allowed".format(
                        error="FileNotAllowed", # TODO create ValidationError
                        file_clean_name=f.filename)
            raise LudoboxError(message)

def write_attachments(attachments, game_path):
    """Write all files contains in attachements into game directory"""

    # Check files
    check_attachments(attachments)

    # Create a directory to store the uploaded files
    attachments_path = os.path.join(game_path, "files")
    try:
        if not os.path.exists(attachments_path):
            os.makedirs(attachments_path)
    except Exception as e:
        message = "<Error> occured while "\
                  "writing game info to path '{path}'. "\
                  "Impossible to create "\
                  "directory '{attachments_path}' to store the attached "\
                  "files.".format(
                    path=game_path,
                    attachments_path=os.path.abspath(attachments_path))
        raise LudoboxError(message)

    # Write all the files
    for f in attachments:
        file_clean_name = secure_filename(f.filename)
        file_path = os.path.join(attachments_path, file_clean_name)
        current_app.logger.debug("saving  %s"%file_path)
        try:
            f.save(file_path)
        except Exception as e:
            message = "<{error}> occured while "\
                      "writing game info to path '{path}'."\
                      "Impossible to save file"\
                      "'{file_path}' in the attachment directory "\
                      "'{attachments_path}'.".format(
                        error=e.strerror,
                        path=data_dir,
                        file_path=os.path.abspath(file_path),
                        attachments_path=os.path.abspath(attachments_path))
            raise LudoboxError(message)

def store_files(game_path, attachments):
    """
    Write files

    - attachments: files to be uploaded to the game folder
    - path
    """
    current_app.logger.debug("attached files : %s"%attachments)

    # Write the attached files
    if attachments:
        try :
            write_attachments(attachments, game_path)
        except LudoboxError as e:
            raise LudoboxError(str(e))

    return game_path

def delete_file(file_path):
    """Delete a file based on its path"""
    try:
        os.remove(file_path)
    except OSError:
        pass
    return file_path

def get_attachements_list(slug):
    content_path = os.path.join(current_app.config["DATA_DIR"], slug)
    files_path = os.path.join(content_path,"files")
    if os.path.exists(files_path):
        file_list = os.listdir(files_path)
    else :
        file_list = []
    return file_list
