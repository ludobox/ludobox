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
import time

import json

from flask import current_app

from jsonpatch import make_patch, JsonPatch

# TODO :  implement state changes (draft -> reviewed, etc.)
event_types = ["create", "update", "delete", "change_state"]

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
    ts = int(time.time())

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
    assert type(event["id"]) is str or unicode
    assert len(event["id"]) is 40
    assert type(event["content"]) is dict
    assert type(event["ts"]) is int
    assert event["type"] in event_types
    return True

def add_event_to_history(content_previous_version, event):
    """
    Does 3 things :
    - create threaded history of events if empty
    - add current event to history
    - replace old content by the new
    """
    assert is_valid_event(event)

    # immutable: clone original reference
    content_with_updated_history = content_previous_version.copy()

    # init history if empty
    if "history" not in content_with_updated_history.keys():
        content_with_updated_history["history"] = []

    # re-apply changes and store last version
    if event["type"] == "update":
        content_with_updated_history = apply_update_patch(content_with_updated_history, event)
    elif event["type"] == "change_state":
        new_state = event["content"]["to"]
        content_with_updated_history["state"] = new_state

    # add event to history
    content_with_updated_history["history"].append(event)

    current_app.logger.debug("Event : %s - %s"%(event["type"], content_with_updated_history))
    return content_with_updated_history

def make_create_event(content, user=None):

    # make sure there is no prior history
    if "history" in content.keys() and len(content["history"]) !=0:
        raise ValueError("You are trying to use the CREATE action on a game that already has an history.")

    # check if there is actual changes
    if content is None or len(content.keys()) == 0:
        return None

    # create a new event and add it to history
    event = new_event("create", content.copy(), user)
    return event

def make_update_event(old_content, new_content, user=None):

    # make things immutable
    new = new_content.copy()
    old = old_content.copy()

    # ignore keys we don't want to track in the history events
    ignored_keys = ["history", "files", "errors", "has_errors"]
    for k in ignored_keys:
        new.pop(k, None)
        old.pop(k, None)

    # create json diff
    patch = make_patch(new, old)

    # check if there is actual changes
    if not len(list(patch)) :
        return None

    # create a new event and add it to history
    event = new_event("update", { "changes" : list(patch) }, user)
    return event

def make_update_state_event(old_content, updated_content_state, user=None):
    """Store an event reflecting content update"""

    original_state = old_content["state"]

    state_change = { "from" : original_state, "to" : updated_content_state}

    # create a new event and add it to history
    event = new_event("change_state", state_change, user)
    return event

def apply_update_patch(content, event):
    """Apply JSON diff patches to content"""
    patch = JsonPatch(event["content"]["changes"])
    final_content = patch.apply(content)
    return final_content

def apply_history(history, selected_id):
    """
    Re-apply the chain of events from the history until selected id

    returns the content *without* the history
    """

    # check the hash format
    assert type(selected_id) is str
    assert len(selected_id) is 40

    # filter history
    final_content = {}

    # run again the course of events
    for event in history:
        if not is_valid_event(event) :
            raise ValueError("Event does not follow a proper format.")

        # check event type
        if event["type"] == "create": # init with full content
            final_content = event["content"]
        elif event["type"] == "update":
            final_content = apply_update_patch(final_content, event)
        elif event["type"] == "change_state":
            new_state = event["content"]["to"]

        # run until last is
        if event["id"] == selected_id :
            return final_content
