#!/usr/bin/env python
# -*- coding: utf-8 -*-


from jinja2 import Environment, FileSystemLoader
import os
import json
from slugify import slugify

accepted_types=["jpg","png","gif", "stl", "pdf"]

data_dir = os.path.join(os.getcwd(), "data")
games_dir = os.path.join(os.getcwd(), "games")

# Read templates from files
env = Environment(loader=FileSystemLoader('templates'))
# main_template = env.get_template('main.html')  #
single_template = env.get_template('single.html') # display a single game
index_template = env.get_template('index.html') # list all games 
add_template = env.get_template('add.html') # create new game

# create games dir 
if not os.path.exists(games_dir):
    os.makedirs(games_dir)

# store all json game
games = []

# list all folders in "games"
for path in os.listdir(data_dir): 
    if os.path.isdir(os.path.join(data_dir, path)): # check all dir

        # parse game dir 
        data_path = os.path.join(data_dir, path)
        print data_path

        # load json
        json_path = os.path.join(data_path, "info.json")
        with open(json_path, "r") as json_file : 
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
        with open(single_index_path , "wb") as single_index :
            single_index.write(single.encode('utf-8'))

# write root index.html
index = index_template.render({"games" : games}) # pass games as a dict to jinja2
main_index_path = os.path.join(games_dir, "index.html")

with open(main_index_path , "wb") as main_index :
    main_index.write(index.encode('utf-8'))

# write add page
add = add_template.render() # pass games as a dict to jinja2
add_path = os.path.join(games_dir, "add")

# create /new path
if not os.path.exists(add_path):
    os.makedirs(add_path)

# create add game form
with open(os.path.join(add_path, "index.html") , "wb") as add_file :
    add_file.write(add.encode('utf-8'))

