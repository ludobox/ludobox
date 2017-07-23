#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""
This file regoups all operations related to content states

Content states are :
- needs review
- validated
- rejected

"""

from ludobox.errors import LudoboxError
from ludobox.content import read_content, update_content_info

content_states = ["needs_review", "validated", "rejected"]


def is_valid_content_state(content_state):
    """Just to make sure the content_state exists"""
    return content_state in content_states

def is_valid_state_change(old_state, new_state):
    """Check if state has changed and follow the workflow"""
    return old_state != new_state and is_valid_content_state(new_state)

def validates(resource_path):
    new_info = update_content_state(resource_path, "validated")
    return  new_info

def rejects(info):
    new_info = update_content_state(resource_path, "rejected")
    return  new_info

def update_content_state(resource_path, new_state):

    # get current state
    info = read_content(resource_path)
    old_state = info["state"]

    # validate state change
    if not is_valid_state_change(old_state, new_state):
        raise LudoboxError("<Wrong State> Can not update state content to the same state.")

    # update info
    new_info = info.copy()
    new_info["state"] = new_state

    new_content = update_content_info(resource_path, new_info, state=new_state)

    return new_content
