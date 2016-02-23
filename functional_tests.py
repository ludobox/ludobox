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

# TODO work in a temp dir for convenience
# TODO do more in depth testing : output, dir and file created
def test_generate_all_on_hackathon_data():
    # First we clean the rep
    assert ludocore.main("clean")
    # Then we generate everything
    assert ludocore.main("generate")
