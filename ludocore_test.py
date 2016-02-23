#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Here are all the unit tests for the :mod:`ludocore` module.

The objective of those test is to check all major usage scenarios for each
function of the :mod:`ludocore` module.
"""

# Python 3 compatibility
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# The functions to test
from ludocore import generate_all

# For file name manipulations
import os.path

# To help generate convenient temp directories
import tempfile

# To make advanced directory comparisons
import filecmp


def test_generate_all_on_non_empty_data_dir_and_empty_games_dir():
    # A directory with actual game description JSON files
    data_dir = "tests/functional/data"
    # An empty directory for the output
    games_dir = os.path.join(tempfile.mkdtemp(),"games")

    # Does the function works without error?
    assert generate_all(data_dir, games_dir)

    # Let's go for deep comparison with reference files
    expected_dir = "tests/functional/expected"
    expected_files = [
        "add/index.html",
        "index.html",
        "borgia-le-jeu-malsain/index.html",
        "coucou-le-jeu-sympa/index.html",
        "papa-le-jeu-coquin/index.html"]
    match, mismatch, errors = filecmp.cmpfiles(
        games_dir,
        expected_dir,
        expected_files)
    assert errors == []
    assert mismatch == []
    assert sorted(match) == sorted(expected_files)