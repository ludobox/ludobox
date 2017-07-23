#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A script to reset history with events that are not valid

edit USER_EMAIL to change user attribution.

What this script does :
1. check is there is an history
2. check if events in the history are valid
3. ignore files in case the whole history is valid
4. flag files with invalid history
5. prompt user to reset history on invalid files

Here, to "reset history" means :
1. take the current (latest) state of the file
2. erase all existing events in history
3. add a single "create" event with latest state that will now stands as history

The script will also reset all content state to "needs_review"

"""

import os
import json

from ludobox import create_app
from ludobox.content import get_content_index, read_content, validate_content
from ludobox.flat_files import write_info_json
from ludobox.config import read_config
from ludobox.history import is_valid_event, make_create_event, add_event_to_history

from ludobox.utils import json_serial # convert datetime

config = read_config()

app = create_app()

USER_EMAIL = "admin@ludobox.net"

def confirm_choice():
    confirm = raw_input("history for these games will be reset to zero : Yes or No [y/n] ?")
    if confirm != 'y' and confirm != 'n':
        print("\n Invalid Option. Please Enter a Valid Option.")
        return confirm_choice()
    elif confirm == 'y' :
        return True
    elif confirm == 'n' :
        return False

def confirm_user():
    confirm = raw_input("Games creation will be attributed to %s : Yes or No [y/n] ?"%USER_EMAIL)
    if confirm != 'y' and confirm != 'n':
        print("\n Invalid Option. Please Enter a Valid Option.")
        return confirm_choice()
    elif confirm == 'y' :
        return True
    elif confirm == 'n' :
        return False

needs_update = []

with app.app_context():

    games = get_content_index()

    # read all json file and check for errors
    for game in games:

        game_path = os.path.join(config["data_dir"], game['slug'])
        info = read_content(game_path)
        try :
            flagged = False
            history = info["history"]
            for event in history:
                try :
                    if not is_valid_event(event):
                        flagged = True
                except AssertionError:
                    flagged = True
            if flagged :
                needs_update.append(game_path)
        except KeyError:
            # files with no history
            needs_update.append(game_path)

    print "%s/%s games history need to be updated."%(len(needs_update), len(games))

    if not len(needs_update):
        print "No updates needed."
        exit()

    if not confirm_user():
        exit()

    if confirm_choice():

        # update the actual data
        for game_path in needs_update:
            print game_path
            info = read_content(game_path)

            print "-"*10
            print "%s..."%info["title"]

            # remove history
            info.pop('history', None)

            # make a 'create'
            event = make_create_event(info.copy())

            # add it to history
            info["history"] = [ event]

            # reset state
            info["state"] = "needs_review"

            # validate_content(info)

            write_info_json(info, game_path)
            print "updated."
            print

    print "OK ! done."
