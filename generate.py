#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A python script will generate the following files : a list of all games and a
folder containing info of each game.
"""
# TODO make the code testable by providing a way to pass the input and output
#   folders has parameter to a function

# TODO make the code python3 compatible: print function and some few other

# os and shutil are used for file or directory manipulation
import os
import shutil

# json is used to read game descriptions as they are stored as JSON files for
# easy "low tech" compliant sharing.
import json

# Jinja2 is used as a template engine to generate the list of games as an HTML5
# compliant table.
# To get it: sudo pip install Jinja2
import jinja2

# slugify is used to generate clean HTML/URL compliant strings from any unicode
# string while keeping readability. We use it here to generate clean file name
# for all generated files.
# To get it: sudo pip install python-slugify
from slugify import slugify

ACCEPTED_TYPES=["jpg","png","gif", "stl", "pdf"]

# Input directory where we should find JSON files each describing one game
DATA_DIR = os.path.join(os.getcwd(), "data")

# Output dirrectory where we generate the pages:
#   *   one directory for each game filled with all the revelent data: HTML
#       description of the game, attached files, docmentation...
#   *   the wellcome page that gives access to everything
#   *   the add page that allow us to add a new game
GAMES_DIR = os.path.join(os.getcwd(), "games") # output


# TODO improve this exception by always providing an advice to solve the problem
class LudoboxError(Exception):
    """Base class for all the custom exceptions of the module."""
    def __init__(self, message):
        # without this you may get DeprecationWarning
        self.message = message

        # Call the base class constructor with the parameters it needs
        super(LudoboxError, self).__init__(message)


# TODO test this function with different scenari: inexistant dir, info.json
#   present/absent, with/without attached file
def read_game_info(path):
    """
    Read all the info available about the game stored at the provided path.

    Arguments:
    path -- directory where the game info and data are stored

    Returns (ok, data) where ok is a boolean indicating if the data retrieval
    when well and data is a dictionary containing the game data. If ok is
    ``False`` data is empty. You should always test it first:

    >>> ok, data = read_game_info("stupid_path")
    >>> if not ok:
    ...     print "something went wrong"
    something went wrong

    The game data can come from:
    *   the info.json file
    *   the attached files found in the dir
    *   somme are also computed from other data like a cleaned name suitable for
        url generation (slugified name)
    """
    # Load JSON from the description file of the game
    json_path = os.path.join(path, "info.json")
    try:
        with open(json_path, "r") as json_file:
            data = json.load( json_file )
    except IOError, e:
        return False, {}

    # Add permalink
    data["slug"] = slugify(data["title"])

    return True, data


# TODO add a very simple doctest
# TODO add some test for this function with different scenario: empty/incoherent
#   data, directory already exists...
def generate_game_desc(data, games_dir, template):
    """
    Generate a whole game description in the games directory provided from data
    dictionary.

    The game description generated is composed of:
    *   a game directory named after the game itself. It is created in the games
        directory.
    *   an HTML page describing the whole game generated from a template.

    Arguments:
    data -- a dictionnary with all the informations about the game. Typically it
            has been generated with :func:`read_game_info()`.
    games_dir -- directory where the game directory should be created. It must
                 not contain a directory with the same name as the slugified
                 game name.
    template -- a :mod:`jinja2` template object used to generate the HTML
                description file of the game.

    Raise a `LudoboxError` with a convenient message if anything went wrong. In
    such case no directory is created.
    """
    # TODO append ERROR to the end of the directory name instead of deleting it
    # Create game dir
    game_slug_name = data["slug"]  # Name of the game cleaned
    game_path =  os.path.join(games_dir, game_slug_name)
    try:
        os.makedirs(game_path)
    except os.error as e:
        # TODO Handle more precisely the error and provide an advice for solving
        #   the problem
        # Create a very explicit message to explain the problem
        message = "<{error}> occured while creating directory '{path}'".format(
            error=e.strerror,
            path=e.filename)
        raise LudoboxError(message)

    # Render template
    try:
        html = template.render(data)
    except jinja2.TemplateSyntaxError as e:
        # Cleanup anything previously created
        shutil.rmtree(game_path, ignore_errors=True)
        # Create a very explicit message to explain the problem
        # TODO Handle more precisely the error and provide an advice for solving
        #   the problem
        message = "Error while parsing template file {0.filename} "\
                  "at line {0.line} because {0.message}".format(e)
        raise LudoboxError(message)

    html_index_path = os.path.join(game_path, "index.html")

    # Write game index.html
    try:
        with open(html_index_path , "wb") as html_index:
            html_index.write(html.encode('utf-8'))
    except IOError as e:
        # Cleanup anything previously created
        shutil.rmtree(game_path, ignore_errors=True)
        # TODO Handle more precisely the error and provide an advice for solving
        #   the problem
        # Create a very explicit message to explain the problem
        message = "<{error}> occured while creating game '{game}' index file '{path}'".format(
            error=e.strerror,
            game=game_slug_name,
            path=e.filename)
        raise LudoboxError(e.message)


# TODO split this function in many diffrent small func
def main():
    # TODO move this piece of code closer to where it is needed
    # First we need templates from files
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
    try:
        single_template = env.get_template('single.html') # display a single game
        index_template = env.get_template('index.html') # list all games
        add_template = env.get_template('add.html') # create new game
    except jinja2.TemplateNotFound, e:
        print "Template file", e.name, "does not exist"
        # TODO return a standard error code
        return

    # Then we create the games directory
    if not os.path.exists(GAMES_DIR):
        os.makedirs(GAMES_DIR)

    # This stores all JSON from the different games
    games = []

    # We list all folders in "games" sorted alphabetically
    for path in os.listdir(DATA_DIR):
        data_path = os.path.join(DATA_DIR, path)

        # TODO reverse this test to decrease cyclomatic complexity
        if os.path.isdir(data_path): # check only dir
            print data_path
            # Parse a game directory
            print "\tRead game informations:",

            # TODO replace this by a more pythonic exception handling
            ok, game_data = read_game_info(data_path)

            if not ok:
                print "FAIL"
                continue
            print "SUCCESS"

            # Generate game description
            print "\tGenerate game description:",

            # TODO replace this by a more pythonic exception handling
            try:
                generate_game_desc(game_data, GAMES_DIR, single_template)
            except LudoboxError as e:
                print "FAIL >>", e
                continue
            print "SUCCESS"

            # If everything when fine add the game info to the others
            games.append(game_data)

    # We now write the root index.html
    index = index_template.render({"games" : games}) # pass games as a dict to jinja2
    main_index_path = os.path.join(GAMES_DIR, "index.html")

    with open(main_index_path , "wb") as main_index :
        main_index.write(index.encode('utf-8'))

    # We then write the add page
    add = add_template.render() # pass games as a dict to jinja2
    add_path = os.path.join(GAMES_DIR, "add")

    # create add path
    if not os.path.exists(add_path):
        os.makedirs(add_path)

    # create add game form
    with open(os.path.join(add_path, "index.html") , "wb") as add_file :
        add_file.write(add.encode('utf-8'))


# TODO add a generate action to specificaly launch a generation
# TODO add a clean action to specificaly launch a cleanup of all generated files
# TODO add a default action/help action that describe the usage and actions
if __name__ == "__main__":
    main()
