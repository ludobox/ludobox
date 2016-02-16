#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
# json is used to read game descriptions as they are stored as JSON files for
# easy "low tech" compliant sharing.
import json
# Jinja2 is used as a template engine to generate the list of games as an HTML5
# compliant table.
# To get it: sudo pip install Jinja2
from jinja2 import Environment, FileSystemLoader
# slugify is used to generate clean HTML/URL compliant strings from any unicode
# string while keeping readability. We use it here to generate clean file name
# for all generated files.
# To get it: sudo pip install python-slugify
from slugify import slugify

accepted_types=["jpg","png","gif", "stl", "pdf"]

# Input directory where we should find JSON files each describing one game
data_dir = os.path.join(os.getcwd(), "data")

# Output dirrectory where we generate the pages:
#   *   one directory for each game filled with all the revelent data: HTML
#       description of the game, attached files, docmentation...
#   *   the wellcome page that gives access to everything
#   *   the add page that allow us to add a new game
games_dir = os.path.join(os.getcwd(), "games") # output

def main():
    # First we eead templates from files
    env = Environment(loader=FileSystemLoader('templates'))
    single_template = env.get_template('single.html') # display a single game
    index_template = env.get_template('index.html') # list all games
    add_template = env.get_template('add.html') # create new game

    # Then we create the games directory
    if not os.path.exists(games_dir):
        os.makedirs(games_dir)

    # This stores all JSON from the different games
    games = []

    # We list all folders in "games"
    for path in os.listdir(data_dir):
        if os.path.isdir(os.path.join(data_dir, path)): # check all dir

            # parse game dir
            data_path = os.path.join(data_dir, path)
            print data_path

            # load json
            json_path = os.path.join(data_path, "info.json")
            with open(json_path, "r") as json_file:
                game_data = json.load( json_file )
            games.append(game_data)

            # add permalink
            game_data["slug"] = slugify(game_data["title"])

            # create game dir
            game_path =  os.path.join(games_dir, game_data["slug"])
            if not os.path.exists(game_path):
                os.makedirs(game_path)

            # render template
            single = single_template.render(game_data)
            single_index_path = os.path.join(game_path, "index.html")

            # write game index.html
            with open(single_index_path , "wb") as single_index:
                single_index.write(single.encode('utf-8'))

    # We now write the root index.html
    index = index_template.render({"games" : games}) # pass games as a dict to jinja2
    main_index_path = os.path.join(games_dir, "index.html")

    with open(main_index_path , "wb") as main_index :
        main_index.write(index.encode('utf-8'))

    # We then write the add page
    add = add_template.render() # pass games as a dict to jinja2
    add_path = os.path.join(games_dir, "add")

    # create add path
    if not os.path.exists(add_path):
        os.makedirs(add_path)

    # create add game form
    with open(os.path.join(add_path, "index.html") , "wb") as add_file :
        add_file.write(add.encode('utf-8'))

if __name__ == "__main__":
    main()
