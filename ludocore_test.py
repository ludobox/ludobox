#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Here are all the unit tests for the :mod:`ludocore` module.

The objective of those test is to check all major usage scenarios for each
function of the :mod:`ludocore` module.
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

# Python 3 compatibility
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# The functions to test
from ludocore import generate_all

# For file name manipulations
import os.path

# To make advanced directory comparisons
import filecmp


def test_generate_all_on_non_empty_data_dir_and_empty_games_dir(tmpdir):
    # A directory with actual game description JSON files
    input_dir = "tests/functional/data/hackathon"
    # An empty directory for the output
    output_dir = os.path.join(str(tmpdir), "out")

    # Does the function works without error?
    assert generate_all(input_dir, output_dir)

    # Let's go for deep comparison with reference files
    expected_dir = "tests/functional/expected/on_hackathon_data_dir"
    expected_files = [
        "about.html",
        "add/index.html",
        "index.html",
        "games/borgia-le-jeu-malsain/index.html",
        "games/coucou-le-jeu-sympa/index.html",
        "games/papa-le-jeu-coquin/index.html"]
    match, mismatch, errors = filecmp.cmpfiles(
        output_dir,
        expected_dir,
        expected_files)
    assert errors == []
    assert mismatch == []
    assert sorted(match) == sorted(expected_files)


def test_generate_all_on_empty_data_dir(tmpdir):
    # An empty directory as input data
    input_dir = os.path.join(str(tmpdir), "empty")
    os.makedirs(input_dir)
    # An empty directory for the output
    output_dir = os.path.join(str(tmpdir), "out")

    # Does the function works without error?
    assert generate_all(input_dir, output_dir)

    # Did it generate a games directory ?
    games_dir = os.path.join(output_dir, "games")
    assert os.path.isdir(games_dir)

    # Let's go for deep comparison with reference files
    expected_dir = "tests/functional/expected/on_empty_data_dir"
    expected_files = [
        "about.html",
        "add/index.html",
        "index.html"]
    match, mismatch, errors = filecmp.cmpfiles(
        output_dir,
        expected_dir,
        expected_files)
    assert errors == []
    assert mismatch == []
    assert sorted(match) == sorted(expected_files)

    # Let's be sure we have nothing else in the output dir
    generated = [n for n in os.listdir(output_dir)]
    assert sorted(generated) == sorted(
        ["games", "add", "index.html", "about.html"])
