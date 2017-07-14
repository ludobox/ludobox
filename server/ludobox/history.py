#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Record and manage file changes and keep track of history.

Key concepts are :
- events : everytime somethin is changed, we use this event
- history : the whole thread of events that applies to a page

For each event, a unique SHA id is created (like git https://stackoverflow.com/questions/29106996/git-what-is-a-git-commit-id )
"""

import hashlib
from datetime import datetime

from jsonpatch import make_patch

event_types = ["create", "update", "delete"]

# hashing changes to create an id
sha_1 = hashlib.sha1()

def new_event(event_type, content, user=None):

    if event_type not in event_types:
        raise ValueError(
            "Event type should be one of the following %s"%", ".join(event_types))

    if type(content) is not dict:
        raise ValueError(
            "Event content should be a JSON-compatible object.")

    # timestamp
    ts = datetime.now().isoformat()

    # generate unique ID using the whole content
    sha_1.update("%s - %s - %s - %s"%(event_type, content, user, ts) )
    sha_id = sha_1.hexdigest()

    return {
        "type" : event_type,
        "content" : content,
        "user" : user,
        "id" : sha_id,
        "ts" : ts
    }

def is_valid_event(event):
    assert type(event) is dict
    assert type(event["id"]) is str
    assert len(event["id"]) is 40
    assert type(event["content"]) is dict
    assert event["type"] in event_types
    return True

def add_event_to_history(game_info, event):
    """Create history thread if needed and add current event to it"""
    assert is_valid_event(event)

    # init history if empty
    if "history" not in game_info.keys():
        game_info["history"] = []

    # add event to history
    game_info["history"].append(event)

    return game_info

def event_create(content, user=None):

    # make sure there is no prior history
    if "history" in content.keys() and len(content["history"]) !=0:
        raise ValueError("You are trying to use the CREATE action on a game that already has an history.")

    # check if there is actual changes
    if content is None or len(content.keys()) == 0:
        return None

    # create a new event and add it to history
    event = new_event("create", content, user)
    return event

def event_update(new_content, old_content, user=None):

    # make sure content has no history
    if "history" in new_content.keys() and len(new_content["history"]) !=0:
        raise ValueError("To update, please pass the content only - without the 'history'.")

    if "history" in old_content.keys() and len(old_content["history"]) !=0:
        raise ValueError("To update, please pass the content only - without the 'history'.")

    # create json diff
    patch = make_patch(new_content, old_content)

    # check if there is actual changes
    if not len(list(patch)) :
        return None

    # create a new event and add it to history
    event = new_event("update", { "changes" : list(patch) }, user)
    return event
