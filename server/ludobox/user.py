#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Everything related to user logics : latest_changes, profile, etc.

"""

from ludobox.content import get_content_index
from ludobox.utils import get_resource_slug

from datetime import datetime

def get_latest_changes(user=None, before_time=None):
    """
    Return all latest changes made on files.
    Filter is based on 2 params :
    - user : email of the user
    - time : int in epoch time
    """

    # used for time comparison
    time_limit = None

    # get index with all content
    contents = get_content_index(short=False)

    if before_time is not None:
        assert type(before_time) is int
        time_limit = datetime.fromtimestamp(before_time)

    histories = []
    for content in contents:
        slug = get_resource_slug(content)
        histories.append((
            content["title"],
            content["history"],
            slug
        ))

    lastest_changes = []
    for thread in histories:
        title = thread[0]
        history = thread[1]
        slug = thread[2]
        for event in history:

            # send all events by default
            keep_event = True

            # check if user as specified a time limit
            if time_limit :
                time_event = datetime.fromtimestamp(event["ts"])
                # check if the event should be included
                if time_event > time_limit   :
                    keep_event = False

            if user and event["user"] != user :
                keep_event = False

            # store events
            if keep_event:
                lastest_changes.append(
                    {
                        "title" : title,
                        "event" : event,
                        "slug" : slug
                    }
                )

    return lastest_changes
