#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Update slug to a more complete using content_type and language code

How it works :

- Scan /data folder and check is slug and folders are correct.
- If not, flag for update
- Ask user for confirmation (y/n)
- Rewrite info.json with the right slug
- Rename folder with the right slug

"""

import os
import ludobox

from ludobox import create_app
from ludobox.content import read_content
from ludobox.utils import get_resource_slug
from ludobox.flat_files import write_info_json

data_dir = os.path.join(os.getcwd(),"data")
print "CHANGES : %s"%data_dir
print "-"*10

app = create_app()

to_update = []

def confirm_choice():
    confirm = raw_input( "Add 'needs_review' state to these %s folder(s) : Yes or No [y/n] ?" %len(to_update) )
    if confirm != 'y' and confirm != 'n':
        print("\n Invalid Option. Please Enter a Valid Option.")
        return confirm_choice()
    elif confirm == 'y' :
        return True
    elif confirm == 'n' :
        return False

if __name__ == '__main__':

    with app.app_context():

        renames = []
        for game_folder_name in os.listdir(data_dir) :
            game_path = os.path.join(data_dir,game_folder_name)
            if os.path.isdir(game_path):
                info = read_content(game_path)
                if "state" not in info.keys():
                    to_update.append((game_path,info))

        if not len(to_update):
            print "No updates needed."
            exit()

        if confirm_choice():
            for game_path, info in to_update:

                # remove file lists
                info["state"] = "needs_review"
                info.pop('files', None)

                write_info_json(info, game_path)

            print "%s content states added."%len(to_update)
        else :
            print 'Operation cancelled'
