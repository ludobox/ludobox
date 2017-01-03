#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A python script will generate the following files : a list of all games and a
folder containing info of each game.
"""
# Copyright (C) 2016  Pierre-Yves Martin for DCALK
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# TODO make the code testable by providing a way to pass the input and output
#   folders has parameter to a function

# Python 3 compatibility
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# Used for file or directory manipulation
import os
import shutil
import glob

# json is used to read game descriptions as they are stored as JSON files for
# easy "low tech" compliant sharing.
import json

# datetime is used to generate a simple timestamp for each game added
from datetime import datetime

# Jinja2 is used as a template engine to generate the list of games as an HTML5
# compliant table.
# To get it: sudo pip install Jinja2
import jinja2

from ludobox.content import read_game_info
from ludobox.errors import LudoboxError

# read config file
from ludobox.config import read_config
config=read_config()

# Input directory where we should find JSON files each describing one game
INPUT_DIR = os.path.abspath("data")

# Output directory where we generate the pages:
#   *   one directory for each game filled with all the revelent data: HTML
#       description of the game, attached files, docmentation...
#   *   the wellcome page that gives access to everything
#   *   the add page that allow us to add a new game
OUTPUT_DIR = os.path.abspath("static")

# Directory where all the template files are stored
TEMPLATE_DIR = os.path.abspath("templates")
SINGLE_TEMPLATE = "single.html"  # template for page to display a single game
INDEX_TEMPLATE = "index.html"  # template for page to list all games
ADD_TEMPLATE = "add.html"  # template for page to create new game
ABOUT_TEMPLATE = "about.html"  # template for the about page




# TODO replace this by a call to automatic template renderer func
def _render_template(tpl_name, data={}, games=[]):
    """
    Encapsulate the rendering of a Jinja2 template.

    This function create a Jinja2 environnement and use it to render the
    specified template. The fact to use a new environment fr each template
    while they are all stored in the same directory helps us to provide more
    testable functions (by a reducing coupling).

    Arguments:
    tpl_name -- name of the template to render. It must be the name of a file
                in the template directory `TEMPLATE_DIR`.
    data -- a dictionary containing all the descriptions of one game. Used only
            if rendering a specific game page. Default to empty dictionnary.
    games -- a list of all the games descriptions. Used only if rendering
             global index. Default to empty list.

    Returns a string containing the ready-to-use HTML code rendered by Jinja2.

    Raise a :exc:`LudoboxError` with a convenient message if anything went
    wrong.
    """

    try:
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR))
    except Exception as e:  # I've no idea what kind of exception can be raised
        message = "Error while creating environnemnt for templates from "\
                  "directory '{dir}'".format(dir=TEMPLATE_DIR)
        raise LudoboxError(message)

    try:
        template = env.get_template(tpl_name)
    except jinja2.TemplateNotFound, e:
        message = "Template file '{tpl}' does not exist".format(tpl=e.name)
        raise LudoboxError(message)

    try:
        html = template.render(data=data, games=games)
    except jinja2.TemplateSyntaxError as e:
        # Cleanup anything previously created
        shutil.rmtree(game_path, ignore_errors=True)
        # Create a very explicit message to explain the problem
        # TODO Handle more precisely the error and provide an advice for
        #   solving the problem
        message = "Error while parsing template file {0.filename} "\
                  "at line {0.line} because {0.message}".format(e)
        raise LudoboxError(message)

    # If everything was ok then we return the html
    return html


# TODO append ERROR to the end of the directory name instead of deleting it
# TODO add some test for this function with different scenario:
#   empty/incoherent data/are nor readable, directory already exists/is read
#   only...
def generate_game_desc(data, games_dir, tpl_name):
    """
    Generate a game description in the games directory provided from data dict.

    The game description generated is composed of:
    *   a game directory named after the game itself. It is created in the
        `games_dir` directory.
    *   an HTML page describing the whole game generated from a template.

    Arguments:
    data -- a dictionnary with all the informations about the game. Typically
            it has been generated with :func:`read_game_info()`.
    games_dir -- directory where the game directories should be created. It
                 must not contain a directory with the same name as any
                 slugified game name.
    tpl_name -- a :mod:`jinja2` template file used to generate the HTML
                description file. It must be located in the `TEMPLATE_DIR`
                directory.

    Raise a :exc:`LudoboxError` with a convenient message if anything went
    wrong. In such case no directory is created.

    Typical usage:

    >>> data = read_game_info("tests/functional/data/hackathon/borgia-le-jeu-malsain")
    >>> import tempfile
    >>> import os.path
    >>> games_dir = os.path.join(tempfile.mkdtemp(),"games")
    >>> generate_game_desc(data, games_dir, "single.html")
    """
    # Name of the game cleaned
    game_slug_name = data["slug"]

    # Create game dir
    game_path = os.path.join(games_dir, game_slug_name)
    try:
        os.makedirs(game_path)
    except os.error as e:
        # TODO Handle more precisely the error and provide an advice for
        #   solving the problem
        # Create a very explicit message to explain the problem
        message = "<{error}> occured while creating directory '{path}'".format(
            error=e.strerror,
            path=e.filename)
        raise LudoboxError(message)

    # TODO enclose in a try/except block to catch the exception and add some
    #   context/better advice
    # Render template
    content = _render_template(tpl_name, data=data)

    path = os.path.join(game_path, "index.html")

    # Write game index.html
    try:
        with open(path, "wb") as f:
            f.write(content.encode('utf-8'))
    except IOError as e:
        # Cleanup anything previously created
        # TODO use clean(game=game_name)
        shutil.rmtree(game_path, ignore_errors=True)
        # TODO Handle more precisely the error and provide an advice for
        #   solving the problem
        # Create a very explicit message to explain the problem
        message = "<{error}> occured while "\
                  "creating game '{game}' index file '{path}'".format(
                    error=e.strerror,
                    game=game_slug_name,
                    path=e.filename)
        raise LudoboxError(message)


# TODO add some test for this function with different scenario: index already
#   exists/or not/is read-only, games dir exist/or not/is read only...
def render_index(games, games_dir, tpl_name):
    """
    Render the index file containing the listing of all the games.

    This file is created in the specified `games_dir` and is always named
    `index.html`.

    Arguments:
    games -- a list which each element is the description of a game. Typically
             each of those elements have been produced by
             :func:`generate_game_desc`.
    games_dir -- directory where the index file will be created. It must
                 not contain an `index.html` file. It must exist.
    tpl_name -- a :mod:`jinja2` template file used to generate the HTML
                index file. It must be located in the `TEMPLATE_DIR` directory.

    Raise a :exc:`LudoboxError` with a convenient message if anything went
    wrong. In such case no index file is created.

    Typical usage:

    >>> games = [read_game_info("tests/functional/data/hackathon/borgia-le-jeu-malsain")]
    >>> import tempfile
    >>> import os.path
    >>> import os
    >>> games_dir = os.path.join(tempfile.mkdtemp(),"games")
    >>> os.makedirs(games_dir)  # The games directory must exist
    >>> render_index(games, games_dir, "index.html")
    """
    # TODO enclose in a try/except block to catch the exception and add some
    #   context/better advice
    # Render template
    content = _render_template(tpl_name, games=games)

    path = os.path.join(games_dir, "index.html")

    # Check if there is already an existing index file
    if os.path.exists(path):
        message = "Can not create global index file '{path}' since a file of "\
                  "same name already exists.".format(path=path)
        raise LudoboxError(message)

    # We write the content to the file
    try:
        with open(path, "wb") as f:
            f.write(content.encode('utf-8'))
    except IOError as e:
        # TODO Handle more precisely the error and provide an advice for
        #   solving the problem
        # Create a very explicit message to explain the problem
        message = "<{error}> occured while creating global index "\
                  "file '{path}'".format(
                    error=e.strerror,
                    path=e.filename)
        raise LudoboxError(message)


# TODO add some test for this function with different scenario: index already
#   exists/or not/is read-only, add dir exist/or not/is read only...
def render_add(games_dir, tpl_name):
    """
    Render the add page used to add a new game to the base via a form.

    This file is created in a subdirectory `add` created in the specified
    `games_dir` and is always named `add/index.html`.

    Arguments:
    games_dir -- directory where the add page file will be created. It must
                 contain neither an `add` directory nor an `add/index.html`
                 file.
    tpl_name -- a :mod:`jinja2` template file used to generate the HTML add
                file. It must be located in the `TEMPLATE_DIR` directory.

    Raise a :exc:`LudoboxError` with a convenient message if anything went
    wrong. In such case no directory or file is created.

    Typical usage:

    >>> import tempfile
    >>> import os.path
    >>> import os
    >>> games_dir = os.path.join(tempfile.mkdtemp(),"games")
    >>> os.makedirs(games_dir)  # The games directory must exist
    >>> render_add(games_dir, "add.html")
    """
    # TODO enclose in a try/except block to catch the exception and add some
    #   context/better advice
    # Render template
    content = _render_template(tpl_name)

    path = os.path.join(games_dir, "add")

    # create add path
    try:
        os.makedirs(path)
    except os.error as e:
        # TODO Handle more precisely the error and provide an advice for
        #   solving the problem
        # Create a very explicit message to explain the problem
        message = "<{error}> occured while creating directory '{path}'".format(
            error=e.strerror,
            path=e.filename)
        raise LudoboxError(message)

    # create add game form
    try:
        with open(os.path.join(path, "index.html"), "wb") as f:
            f.write(content.encode('utf-8'))
    except IOError as e:
        # TODO Handle more precisely the error and provide an advice for
        #   solving the problem
        # Create a very explicit message to explain the problem
        message = "<{error}> occured while creating add page index "\
                  "file '{path}'".format(
                    error=e.strerror,
                    path=e.filename)
        raise LudoboxError(message)


# TODO add some test for this function with different scenario: index already
#   exists/or not/is read-only, add dir exist/or not/is read only...
def render_about(games_dir, tpl_name):
    """
    Render the about page.

    This file is created in the specified `games_dir` and is always named
    `about.html`.

    Arguments:
    games_dir -- directory where the about file will be created. It must
                 not contain an `about.html` file. It must exist.
    tpl_name -- a :mod:`jinja2` template file used to generate the HTML about
                file. It must be located in the `TEMPLATE_DIR` directory.

    Raise a :exc:`LudoboxError` with a convenient message if anything went
    wrong. In such case no directory or file is created.

    Typical usage:

    >>> import tempfile
    >>> import os.path
    >>> import os
    >>> games_dir = os.path.join(tempfile.mkdtemp(),"games")
    >>> os.makedirs(games_dir)  # The games directory must exist
    >>> render_about(games_dir, "about.html")
    """
    # TODO enclose in a try/except block to catch the exception and add some
    #   context/better advice
    # Render template
    content = _render_template(tpl_name)

    path = os.path.join(games_dir, "about.html")

    # Check if there is already an existing about file
    if os.path.exists(path):
        message = "Can not create about file '{path}' since a file of "\
                  "same name already exists.".format(path=path)
        raise LudoboxError(message)

    # We write the content to the file
    try:
        with open(path, "wb") as f:
            f.write(content.encode('utf-8'))
    except IOError as e:
        # TODO Handle more precisely the error and provide an advice for
        #   solving the problem
        # Create a very explicit message to explain the problem
        message = "<{error}> occured while creating about page "\
                  "file '{path}'".format(
                    error=e.strerror,
                    path=e.filename)
        raise LudoboxError(message)


def generate_all(input_dir, output_dir, **kwargs):
    """
    Generate all the pages corresponding to the data of the :const:`DATADIR`.

    It also generates a global index giving access to all the game pages and a
    page to add a new game.

    Keyword arguments:
    input_dir -- directory where the game info and data are stored. It will
                 only be read. And it must exist.
    output_dir -- directory where the games subdirectory (where all game pages
                  will be created), global index, add page and about page will
                  be created. It must not contain a subdirectory named `add`,
                  `games` or an `index.html` or `about.html` file.

    kwargs is used here since this function is called by :func:`main` via
    :mod:`argparse`. And all the params are provided automagically by
    :func:`argparse.ArgumentParser.parse_args` converted to a dict using
    :func:`vars`.
    See `Namespace object<https://docs.python.org/2/library/argparse.html#the-namespace-object>`_

    Returns ``True`` if all generations are a success ``False`` otherwise. This
    result is useful for testing pupose.

    Typical usage:

    >>> import tempfile
    >>> import os.path
    >>> games_dir = os.path.join(tempfile.mkdtemp(),"games")
    >>> generate_all("tests/functional/data/hackathon", games_dir)
    Create games directory: SUCCESS
    borgia-le-jeu-malsain
        Read game informations: SUCCESS
        Generate game description: SUCCESS
    coucou-le-jeu-sympa
        Read game informations: SUCCESS
        Generate game description: SUCCESS
    papa-le-jeu-coquin
        Read game informations: SUCCESS
        Generate game description: SUCCESS
    Generate global index: SUCCESS
    Generate add page: SUCCESS
    Generate about page: SUCCESS
    True
    """
    # Return value, will be switched to False in case of failure
    result = True
    # This stores all JSON from the different games
    games = []

    # We first create a games subdirectory
    print("Create games directory: ", end='')
    games_dir = os.path.join(output_dir, "games")
    if os.path.exists(games_dir):
        message = "'{path}' already exist impossible to create it.".format(
            path=games_dir)
        advice = "Try to use './ludocore.py clean' to remove it."
        print("FAIL >>", message, advice)
        result = False
    else:
        try:
            os.makedirs(games_dir)
            print("SUCCESS")
        except os.error as e:
            # TODO Handle more precisely the error and provide an advice for
            #   solving the problem
            # Create a very explicit message to explain the problem
            message = "<{error}> occured while creating directory "\
                      "'{path}'".format(
                        error=e.strerror,
                        path=e.filename)
            print("FAIL >>", message, advice)
            result = False

    # We list all folders in "games" sorted alphabetically
    for path in sorted(os.listdir(input_dir)):
        data_path = os.path.join(input_dir, path)
        if os.path.isdir(data_path) and os.path.basename(data_path) != "index":
            # Print the name of the game we are taking care of...
            print(os.path.basename(data_path))

            # Parse a game directory
            print("    Read game informations: ", end='')
            try:
                game_data = read_game_info(data_path)
            except LudoboxError as e:
                print("FAIL >>", e)
                result = False
                continue
            print("SUCCESS")

            # Generate game description
            print("    Generate game description: ", end='')
            try:
                generate_game_desc(game_data, games_dir, SINGLE_TEMPLATE)
            except LudoboxError as e:
                advice = "Try to use './ludocore.py clean' to remove it."
                print("FAIL >>", e, advice)
                result = False
                continue
            print("SUCCESS")

            # If everything when fine add the game info to the others
            games.append(game_data)

    # We now write the root index.html
    print("Generate global index: ", end='')
    try:
        render_index(games, output_dir, INDEX_TEMPLATE)
        print("SUCCESS")
    except LudoboxError as e:
        print("FAIL >>", e)
        result = False
        # No need to stop the execution we continue since following action
        # don't depend on the result of this one

    # Check if adding game is allowed
    if config["upload_allowed"] is True:
        # We then write the add page
        print("Generate add page: ", end='')
        try:
            render_add(output_dir, ADD_TEMPLATE)
            print("SUCCESS")
        except LudoboxError as e:
            print("FAIL >>", e)
            result = False
            # No need to stop the execution we continue since following action
            # don't depend on the result of this one

    # We then write the about page
    print("Generate about page: ", end='')
    try:
        render_about(output_dir, ABOUT_TEMPLATE)
        print("SUCCESS")
    except LudoboxError as e:
        print("FAIL >>", e)
        result = False
        # No need to stop the execution we continue since following action
        # don't depend on the result of this one

    return result


# TODO add some counter feedback: XXX games page removed, XXX files removed...
def clean(output_dir, **kwargs):
    """
    Remove all the generated files/directory created by :func:`generate_all`.

    This function will remove:
    *   the `output_dir/index.html` file
    *   the `output_dir/about.html` file
    *   the whole `output_dir/add` directory and its content
    *   the whole `output_dir/games` directory and its content
    *   any *.pyc file generated by previous python execution/test
    *   any *.pyo file generated by previous python execution/test
    *   any __pycache__ files generated by previous python :mod:`py.test`

    Keyword arguments:
    output_dir -- Directory previously used as output for the
                  :func:`generate_all` function.

    kwargs is used here since this function is called by :func:`main` via
    :mod:`argparse`. And all the params are provided automagically by
    :func:`argparse.ArgumentParser.parse_args` converted to a dict using
    :func:`vars`.
    See `Namespace object<https://docs.python.org/2/library/argparse.html#the-namespace-object>`_

    Returns ``True`` if all cleanups are a success ``False`` otherwise. This
    result is useful for testing pupose.

    Typical usage:

    >>> import tempfile
    >>> import os.path
    >>> clean_me_i_m_famous = os.path.join(tempfile.mkdtemp(),"dirty")
    >>> clean(clean_me_i_m_famous)
    Remove all generated pages and directory: SUCCESS
    Remove all precompiled python files (*.pyc): SUCCESS
    Remove all python generated object files (*.pyo): SUCCESS
    Remove py.test caches directory (__pycache__): SUCCESS
    True
    """
    # Return value, will be switched to False in case of failure
    result = True

    print("Remove all generated pages and directory: ", end='')
    games_dir = os.path.join(output_dir, "games")
    shutil.rmtree(games_dir, ignore_errors=True)

    index_file = os.path.join(output_dir, "index.html")
    try:
        os.remove(index_file)
    except OSError as e:
        # TODO handle the error more gently... and with more feedback
        pass

    about_file = os.path.join(output_dir, "about.html")
    try:
        os.remove(about_file)
    except OSError as e:
        # TODO handle the error more gently... and with more feedback
        pass

    add_dir = os.path.join(output_dir, "add")
    shutil.rmtree(add_dir, ignore_errors=True)
    print("SUCCESS")

    print("Remove all precompiled python files (*.pyc): ", end='')
    for f in glob.glob("*.pyc"):
        os.remove(f)
    for f in glob.glob("tests/*.pyc"):
        os.remove(f)
    for f in glob.glob("ludobox/*.pyc"):
        os.remove(f)
    for f in glob.glob("ludobox/data/*.pyc"):
        os.remove(f)
    print("SUCCESS")

    print("Remove all python generated object files (*.pyo): ", end='')
    for f in glob.glob("*.pyo"):
        os.remove(f)
    print("SUCCESS")

    print("Remove py.test caches directory (__pycache__): ", end='')
    shutil.rmtree("__pycache__", ignore_errors=True)
    shutil.rmtree("tests/__pycache__", ignore_errors=True)
    print("SUCCESS")

    return result
