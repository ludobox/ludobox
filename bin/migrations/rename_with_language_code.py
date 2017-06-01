#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import ludobox

from ludobox.content import read_game_info, get_resource_slug

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
            info = read_game_info(path)
            slug = get_resource_slug(info)
            if game_folder_name != slug:
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
        paths = (os.path.join(data_dir,r[0]), os.path.join(data_dir,r[1]))
        print "%s ---> %s"%(paths)
        os.rename(*paths)
    print "%s folder(s) renamed"%len(renames)
else :
    print 'Operation cancelled'
