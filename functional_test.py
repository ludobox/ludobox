#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Here are all the functional tests for the ludobox-ui application.

Those test are based on real life data provided by DCALK team members.

The objective of those test is to check that valid, real life input should
produce valid, real life output. We are not testing for corner cases but only
for actual production cases.
"""

# Python 3 compatibility
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# ludocore
import ludocore

# TODO do more in depth testing : output, dir and file created
def test_generate_all_on_hackathon_data_in_empty_games_directory(tmpdir):
    tmp_games_dir = tmpdir.join("games")

    # Then we generate everything
    assert ludocore.main(
        "generate --input_dir tests/functional/data --output_dir {tmp}".format(
            tmp=tmp_games_dir))


# TODO do more in depth testing : output, dir and file created
def test_generate_all_then_clean_on_hackathon_data(tmpdir):
    tmp_games_dir = tmpdir.join("games")

    # Then we generate everything
    assert ludocore.main(
        "generate --input_dir tests/functional/data --output_dir {tmp}".format(
            tmp=tmp_games_dir))

    # First we clean the rep
    assert ludocore.main(
        "clean --output_dir {tmp}".format(tmp=tmp_games_dir))
