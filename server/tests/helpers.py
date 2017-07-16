#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Useful test to make testing less painfull
"""

import os
import shutil

def delete_data_path(test_data_path):
    # create empy path for data
    if os.path.exists(test_data_path):
        shutil.rmtree(test_data_path)

def create_empty_data_path(test_data_path):
    os.makedirs(test_data_path)

def add_samples_to_data_dir(test_data_path):
    """ Make a temporary data dir with sample games """
    delete_data_path(test_data_path)

    sample_folder = os.path.join(os.getcwd(),"server/tests/test-data")
    shutil.copytree(sample_folder, test_data_path)
