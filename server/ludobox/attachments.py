#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Manipulate attachement files in the ludobox
"""

import os
from werkzeug import secure_filename

from ludobox.errors import LudoboxError

ALLOWED_EXTENSIONS = ["txt", "png", "jpg", "gif", "stl", "zip", "pdf"]

# TODO: improve security check for files !
def allowed_file(filename):
    """Check for valid file extensions"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def write_attachments(attachments, game_path):
    """Write all files contains in attachements into game directory"""

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
        print message
        raise LudoboxError(message)

    # Write all the files
    for f in attachments:
        file_clean_name = secure_filename(f.filename)

        # check if extension is allowed
        # TODO: check for more security issues ?
        if not allowed_file(file_clean_name):
            message = "<{error}> occured while "\
                      "writing. Impossible to save file"\
                      "'{file_clean_name}' because exstension is not allowed".format(
                        error="FileNotAllowed", # TODO create ValidationError
                        file_clean_name=file_clean_name)

            raise LudoboxError(message)

        file_path = os.path.join(attachments_path, file_clean_name)
        print file_path
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
    print attachments

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
