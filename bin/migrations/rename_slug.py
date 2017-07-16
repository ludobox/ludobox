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

from ludobox.content import read_content
from ludobox.utils import get_resource_slug
from ludobox.flat_files import write_info_json

data_dir = os.path.join(os.getcwd(),"data")
print "CHANGES : %s"%data_dir
print "-"*10


renames = []
for game_folder_name in os.listdir(data_dir) :
    path = os.path.join(data_dir,game_folder_name)

    # get only folders
    if os.path.isdir(path):
        info_file = os.path.join(path, "info.json")
        if os.path.exists(info_file):
            info = read_content(path)
            slug = get_resource_slug(info)

            if game_folder_name != slug or "slug" not in info.keys() or info["slug"] != slug:
                renames.append( (game_folder_name, slug) )
                print "'%s' will update to '%s'"%(game_folder_name, slug)

def confirm_choice():
    confirm = raw_input( "Rename these %s folder(s) : Yes or No [y/n] ?" %len(renames) )
    if confirm != 'y' and confirm != 'n':
        print("\n Invalid Option. Please Enter a Valid Option.")
        return confirm_choice()
    elif confirm == 'y' :
        return True
    elif confirm == 'n' :
        return False


if confirm_choice():
    for r in renames:
        # copy
        paths = (os.path.join(data_dir,r[0]), os.path.join(data_dir,r[1]))

        game_path = paths[0]
        info = read_content(game_path)
        slug = get_resource_slug(info)

        # remove file lists
        info["slug"] = slug
        info.pop('files', None)

        write_info_json(info, game_path)

        print "%s ---> %s"%(paths)
        os.rename(*paths)


    print "%s folder(s) renamed"%len(renames)
else :
    print 'Operation cancelled'
