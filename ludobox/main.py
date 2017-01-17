#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse

from ludobox.core import generate_all, clean
from ludobox.testing import autotest
from ludobox.webserver import serve
from ludobox.data import update_data

# TODO: move this to config file
INPUT_DIR = os.path.join(os.getcwd(),"data")
OUTPUT_DIR = os.path.join(os.getcwd(),"static")

# TODO add an info action that list the default dirs, all actual games
#   installed
def config_parser():
    """Configure the argument parser and returns it."""
    # Initialise the parsers
    parser = argparse.ArgumentParser(description="Process some integers.")

    # Add all the actions (subcommands)
    subparsers = parser.add_subparsers(
        title="actions",
        description="the program needs to know what action you want it to do.",
        help="those are all the possible actions")

    # Generate command ########################################################
    parser_generate = subparsers.add_parser(
        "generate",
        help="Generate all the HTML pages by reading the game data")
    parser_generate.set_defaults(func=generate_all)
    parser_generate.add_argument(
        "--input_dir",
        default=INPUT_DIR,
        help="data directory where the game info and data are stored. Default "
             "to {input_dir}".format(input_dir=INPUT_DIR))
    parser_generate.add_argument(
        "--output_dir",
        default=OUTPUT_DIR,
        help="directory where the games subdirectory (where all game pages "
             "will be created), global index and add page will be created. "
             "Default to {output_dir}".format(output_dir=INPUT_DIR))

    # Clean command ###########################################################
    parser_clean = subparsers.add_parser(
        "clean",
        help="Removes all the generated files/directory created by the "
             "'generate' action")
    parser_clean.set_defaults(func=clean)
    parser_clean.add_argument(
        "--output_dir",
        default=OUTPUT_DIR,
        help="Directory previously used as output for the `generate` action. "
             "It's where the games subdirectory (where all game pages will be "
             "created), global index and add page will be created. Default to "
             "{output_dir}".format(output_dir=OUTPUT_DIR))

    # Autotest command ########################################################
    parser_autotest = subparsers.add_parser(
        "autotest",
        help="Execute all the test to check if the program works correctly.")
    parser_autotest.set_defaults(func=autotest)

    # Serve command ###########################################################
    parser_serve = subparsers.add_parser(
        "serve",
        help="Launch an tiny web server to make the ludobox site available.")
    parser_serve.set_defaults(func=serve)
    parser_serve.add_argument(
        "--debug",
        default=False,
        action='store_true',
        help="activate the debug mode of the Flask server (for development "
             "only NEVER use it in production).")
    parser_serve.add_argument(
        "--port",
        default=None,
        help="define port to serve the web application.")

    # Update Data command ###########################################################
    # TODO : parse options to update index only or re-download everything
    parser_data = subparsers.add_parser(
        "data",
        help="Get game data as specified in config files.")
    parser_data.set_defaults(func=update_data)

    # Returns the, now configured, parser
    return parser


def main(commands=None):
    """
    Launch command parser from real command line or from args.

    This allow easy testing of the command line options/actions.
    """
    # Configure the parser
    parser = config_parser()

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
