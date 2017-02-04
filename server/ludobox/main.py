#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import py

from ludobox.webserver import serve

# TODO: move this to config file
INPUT_DIR = os.path.join(os.getcwd(),"data")
OUTPUT_DIR = os.path.join(os.getcwd(),"static")

def test(**kwargs):
    py.test.cmdline.main("server/tests")

# TODO add an info action that list the default dirs, all actual games
#   installed
def config_parser():
    """Configure the argument parser and returns it."""
    # Initialise the parsers
    parser = argparse.ArgumentParser(description="Ludobox server.")

    # Add all the actions (subcommands)
    subparsers = parser.add_subparsers(
        title="actions",
        description="the program needs to know what action you want it to do.",
        help="those are all the possible actions")

    # Test command ###########################################################
    parser_serve = subparsers.add_parser(
        "test",
        help="Run server tests.")
    parser_serve.set_defaults(func=test)

    # Serve command ###########################################################
    parser_serve = subparsers.add_parser(
        "serve",
        help="Launch an tiny web server to make the ludobox site available.")

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
