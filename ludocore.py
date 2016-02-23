#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A python script will generate the following files : a list of all games and a
folder containing info of each game.
"""
# TODO make the code testable by providing a way to pass the input and output
#   folders has parameter to a function

# Python 3 compatibility
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# Used to launch autotests of the program
import doctest
import pytest
# unexported constasts used as pytest.main return codes
# c.f. https://github.com/pytest-dev/pytest/blob/master/_pytest/main.py
PYTEST_EXIT_OK = 0
PYTEST_EXIT_TESTSFAILED = 1
PYTEST_EXIT_INTERRUPTED = 2
PYTEST_EXIT_INTERNALERROR = 3
PYTEST_EXIT_USAGEERROR = 4
PYTEST_EXIT_NOTESTSCOLLECTED = 5

# Used for file or directory manipulation
import os
import shutil
import glob

# Used to handle all the command line mechanics: actions, long params, short
# params...
import argparse

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
DATA_DIR = os.path.abspath("data")

# Output directory where we generate the pages:
#   *   one directory for each game filled with all the revelent data: HTML
#       description of the game, attached files, docmentation...
#   *   the wellcome page that gives access to everything
#   *   the add page that allow us to add a new game
GAMES_DIR = os.path.abspath("games") # output

# Directory where all the template files are stored
TEMPLATE_DIR = os.path.abspath("templates")
SINGLE_TEMPLATE = "single.html"  # template for page to display a single game
INDEX_TEMPLATE = "index.html"  # template for page to list all games
ADD_TEMPLATE = "add.html"  # template for page to create new game

# TODO improve this exception by always providing an advice to solve the problem
# TODO improve this excetion by always providing a context ???
class LudoboxError(Exception):
    """Base class for all the custom exceptions of the module."""
    def __init__(self, message):
        # without this you may get DeprecationWarning
        self.message = message

        # Call the base class constructor with the parameters it needs
        super(LudoboxError, self).__init__(message)


def _render_template(tpl_name, data={}):
    """
    Encapsulate the rendering of a Jinja2 template.

    This function create a Jinja2 environnement and use it to render the
    specified template. The fact to use a new environment fr each template while
    they are all stored in the same directory helps us to provide more testable
    functions (by a reducing coupling).

    Arguments:
    tpl_name -- name of the template to render. It must be the name of a file in
                the template directory `TEMPLATE_DIR`.
    data -- a dictionary with all the keys needed to render the template.
            Defaults to empty dictionary.

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

    # If everything was ok then we return the html
    return html


# TODO test this function with different scenari: existant/inexistant/not
#   readable dir, info.json present/absent/not readable, with/without attached
#   file
def read_game_info(path):
    """
    Read all the info available about the game stored at the provided path.

    Arguments:
    path -- directory where the game info and data are stored

    Returns a dictionary containing the game data.

    >>> data = read_game_info("tests/functional/data/borgia-le-jeu-malsain")
    >>> print(data['audience'])
    Adultes
    >>> print(data['authors'])
    René
    >>> print(data['themes'])
    Médiéval, Salopard

    If anythin goes wrong raise a LudoboxError containing description of the
    error and advice for fixing it.

    >>> try:
    ...     data = read_game_info("stupid_path/no_game")
    ... except LudoboxError as e:
    ...     print(e.message)
    <No such file or directory> occured while reading game 'no_game' info file 'stupid_path/no_game/info.json'

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
            data = json.load(json_file)
    except IOError as e:
        # TODO Handle more precisely the error and provide an advice for solving
        #   the problem
        # Create a very explicit message to explain the problem
        message = "<{error}> occured while "\
                  "reading game '{game}' info file '{json}'".format(
            error=e.strerror,
            game=os.path.basename(path),
            json=e.filename)
        raise LudoboxError(message)

    # TODO Add some attachment info

    # Add permalink
    data["slug"] = slugify(data["title"])

    return data


# TODO append ERROR to the end of the directory name instead of deleting it
# TODO add some test for this function with different scenario: empty/incoherent
#   data/are nor readable, directory already exists/is read only...
def generate_game_desc(data, games_dir, tpl_name):
    """
    Generate a whole game description in the games directory provided from data
    dictionary.

    The game description generated is composed of:
    *   a game directory named after the game itself. It is created in the
        `games_dir` directory.
    *   an HTML page describing the whole game generated from a template.

    Arguments:
    data -- a dictionnary with all the informations about the game. Typically it
            has been generated with :func:`read_game_info()`.
    games_dir -- directory where the game directories should be created. It must
                 not contain a directory with the same name as any slugified
                 game name.
    tpl_name -- a :mod:`jinja2` template file used to generate the HTML
                description file. It must be located in the `TEMPLATE_DIR`
                directory.

    Raise a :exc:`LudoboxError` with a convenient message if anything went
    wrong. In such case no directory is created.

    Typical usage:

    >>> data = read_game_info("tests/functional/data/borgia-le-jeu-malsain")
    >>> import tempfile
    >>> import os.path
    >>> games_dir = os.path.join(tempfile.mkdtemp(),"games")
    >>> generate_game_desc(data, games_dir, "single.html")
    """
    # Name of the game cleaned
    game_slug_name = data["slug"]

    # Create game dir
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

    # TODO enclose in a try/except block to catch the exception and add some
    #   context/better advice
    # Render template
    content = _render_template(tpl_name, data)

    path = os.path.join(game_path, "index.html")

    # Write game index.html
    try:
        with open(path , "wb") as f:
            f.write(content.encode('utf-8'))
    except IOError as e:
        # Cleanup anything previously created
        # TODO use clean(game=game_name)
        shutil.rmtree(game_path, ignore_errors=True)
        # TODO Handle more precisely the error and provide an advice for solving
        #   the problem
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
                 not contain an `index.html` file.
    tpl_name -- a :mod:`jinja2` template file used to generate the HTML
                index file. It must be located in the `TEMPLATE_DIR` directory.

    Raise a :exc:`LudoboxError` with a convenient message if anything went
    wrong. In such case no index file is created.

    Typical usage:

    >>> games = [read_game_info("tests/functional/data/borgia-le-jeu-malsain")]
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
    content = _render_template(tpl_name)

    path = os.path.join(games_dir, "index.html")

    # Check if there is already an existing index file
    if os.path.exists(path):
        message = "Can not create global index file '{path}' since a file of "\
                  "same name already exists.".format(path=path)
        raise LudoboxError(message)

    # We write the content to the file
    try:
        with open(path , "wb") as f :
            f.write(content.encode('utf-8'))
    except IOError as e:
        # TODO Handle more precisely the error and provide an advice for solving
        #   the problem
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
        # TODO Handle more precisely the error and provide an advice for solving
        #   the problem
        # Create a very explicit message to explain the problem
        message = "<{error}> occured while creating directory '{path}'".format(
            error=e.strerror,
            path=e.filename)
        raise LudoboxError(message)

    # create add game form
    try:
        with open(os.path.join(path, "index.html") , "wb") as f :
            f.write(content.encode('utf-8'))
    except IOError as e:
        # TODO Handle more precisely the error and provide an advice for solving
        #   the problem
        # Create a very explicit message to explain the problem
        message = "<{error}> occured while creating add page index "\
                  "file '{path}'".format(
            error=e.strerror,
            path=e.filename)
        raise LudoboxError(message)


# FIXME this does not work if the GAMES_DIR is empty : Generate global index: FAIL >> <No such file or directory> occured while creating global index file '/home/pym/Documents/DCALK/LudoBox/ludobox-ui/games/index.html'
def generate_all(data_dir, games_dir, **kwargs):
    """
    Generate all the pages corresponding to the data of the :const:`DATADIR`. It
    also generates a global index giving access to all the game pages and a page
    to add a new game.

    Keyword arguments:
    data_dir -- directory where the game info and data are stored. It will only
                be read.
    games_dir -- directory where the game directories, global index and add page
                 will be created. It must not contain directories with the same
                 name as any of the slugified game names. It must not contain an
                 directory named `add` or an `index.html` file.

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
    >>> generate_all("tests/functional/data", games_dir)
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
    True
    """
    # Return value, will be switched to False in case of failure
    result = True
    # This stores all JSON from the different games
    games = []

    # We list all folders in "games" sorted alphabetically
    for path in sorted(os.listdir(data_dir)):
        data_path = os.path.join(data_dir, path)
        if os.path.isdir(data_path):
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
                print("FAIL >>", e)
                result = False
                continue
            print("SUCCESS")

            # If everything when fine add the game info to the others
            games.append(game_data)

    # We now write the root index.html
    print("Generate global index: ", end='')
    try:
        render_index(games, games_dir, INDEX_TEMPLATE)
        print("SUCCESS")
    except LudoboxError as e:
        print("FAIL >>", e)
        result = False
        # No need to stop the execution we continue since following action
        # don't depend on the result of this one

    # We then write the add page
    print("Generate add page: ", end='')
    try:
        render_add(games_dir, ADD_TEMPLATE)
        print("SUCCESS")
    except LudoboxError as e:
        print("FAIL >>", e)
        result = False
        # No need to stop the execution we continue since following action
        # don't depend on the result of this one

    return result


# TODO add some counter feedback: XXX games page removed, XXX files removed...
def clean(games_dir, **kwargs):
    """
    Removes all the generated files/directory created by :func:`generate_all`.

    This function will remove:
    *   the whole `games_dir` directory and its content
    *   any *.pyc file generated by previous python execution/test
    *   any *.pyo file generated by previous python execution/test
    *   any __pycache__ files generated by previous python :mod:`py.test`

    Keyword arguments:
    games_dir -- The games directory to clean. It's the place where the games
                 html representation have been generated. Warning: This
                 directory will be totally removed!

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
    >>> games_dir = os.path.join(tempfile.mkdtemp(),"games")
    >>> clean(games_dir)
    Remove all generated pages and directory: SUCCESS
    Remove all precompiled python files (*.pyc): SUCCESS
    Remove all python generated object files (*.pyo): SUCCESS
    Remove py.test caches directory (__pycache__): SUCCESS
    True
    """
    # Return value, will be switched to False in case of failure
    result = True

    print("Remove all generated pages and directory: ", end='')
    shutil.rmtree(games_dir, ignore_errors=True)
    print("SUCCESS")

    print("Remove all precompiled python files (*.pyc): ", end='')
    for f in glob.glob("*.pyc"):
        os.remove(f)
    # TODO remove the *.pyc files from test
    # TODO remove the *.pyc files from test/functionnal
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


def autotest(**kwargs):
    """
    Execute all the test to check if the program works correctly.

    The tests are:
    *   test from the documentation of the code itself (via :mod:`doctest`
        module). They basically check if the usage of the function has not
        changed. This is the equivalent of doing :command:`python -m doctest -v
        ludocore.py`.
    *   unittest from the `tests` directory. Those test are here to check that
        every function works as expected and that all functionnalities are ok
        even in corner cases. They use :mod:`pytest` module.
    *   functionnal tests that try to replicate actuel usecases. They are
        located in `functional_test.py`. They use :mod:`pytest` module. This is
        the equivalent of doing :command:`py.test --quiet --tb=line
        functional_test.py`

    kwargs is used here since this function is called by :func:`main` via
    :mod:`argparse`. And all the params are provided automagically by
    :func:`argparse.ArgumentParser.parse_args` converted to a dict using
    :func:`vars`.
    See `Namespace object<https://docs.python.org/2/library/argparse.html#the-namespace-object>`_
    """
    # Doctests
    print("DOCTESTS".center(80, '#'))
    print("Tests examples from the documentation".center(80, '-'))
    nb_fails, nb_tests = doctest.testmod(verbose=False)
    nb_oks = nb_tests - nb_fails
    print(nb_oks, "/", nb_tests, "tests are OK.")
    if nb_fails > 0:
        print("FAIL")
        print("     To have more details about the errors you should try the "\
              "command: python -m doctest -v ludocore.py")
    else:
        print("SUCCESS")

    # Unit tests
    print("UNIT TESTS".center(80, '#'))
    print("Tests every functionnality in deep".center(80, '-'))
    unit_result = pytest.main([
        "--quiet",
        "--color=no",
        "--tb=line",
        "ludocore_test.py"])
    if unit_result not in (PYTEST_EXIT_OK, PYTEST_EXIT_NOTESTSCOLLECTED):
        print("FAIL")
        print("     To have more details about the errors you should try the "\
              "command: py.test ludocore_test.py")
    else:
        print("SUCCESS")

    # Functional tests
    print("FUNCTIONAL TESTS".center(80, '#'))
    print("Tests actual real life usage and data".center(80, '-'))
    func_result = pytest.main([
        "--quiet",
        "--color=no",
        "--tb=line",
        "functional_test.py"])
    if func_result not in (PYTEST_EXIT_OK, PYTEST_EXIT_NOTESTSCOLLECTED):
        print("FAIL")
        print("     To have more details about the errors you should try the "\
              "command: py.test functional_test.py")
    else:
        print("SUCCESS")


# TODO add an info action that list the default dirs, all actual games installed
def _config_parser():
    """
    Configure the argument parser and returns it.
    """
    # Initialise the parsers
    parser = argparse.ArgumentParser(description="Process some integers.")

    # Add all the actions (subcommands)
    subparsers = parser.add_subparsers(
        title="actions",
        description="the program needs to know what action you want it to do.",
        help="those are all the possible actions")

    # Generate command #########################################################
    parser_generate = subparsers.add_parser(
        "generate",
        help="Generate all the HTML pages by reading the game data")
    parser_generate.set_defaults(func=generate_all)
    parser_generate.add_argument(
        "--data_dir",
        default=DATA_DIR,
        help="data directory where the game info and data are stored. Default "\
             "to {data_dir}".format(
                data_dir=DATA_DIR))
    parser_generate.add_argument(
        "--games_dir",
        default=GAMES_DIR,
        help="directory where the game directories, global index and add page "\
             "will be created. Default to {games_dir}".format(
                games_dir=DATA_DIR))

    # Clean command ############################################################
    parser_clean = subparsers.add_parser(
        "clean",
        help="Removes all the generated files/directory created by the "\
             "'generate' action")
    parser_clean.set_defaults(func=clean)
    parser_clean.add_argument(
        "--games_dir",
        default=GAMES_DIR,
        help="Directory where the games html representation have been "\
             "generated. It will be totally removed. Default "\
             "to {games_dir}".format(
                games_dir=GAMES_DIR))

    # Autotest command #########################################################
    parser_autotest = subparsers.add_parser(
        "autotest",
        help="Execute all the test to check if the program works correctly.")
    parser_autotest.set_defaults(func=autotest)

    # Returns the, now configured, parser
    return parser


def main(commands=None):
    # Configure the parser
    parser = _config_parser()

    # Parse the args
    if commands is None:
        # When executed has a script
        args = parser.parse_args()
    else:
        # When executed in the tests
        args = parser.parse_args(commands.split())

    # Call whatever function was selected
    return args.func(**vars(args))  # We use `vars` to convert args to a dict


if __name__ == "__main__":
    main()
