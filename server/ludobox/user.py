#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Everything related to user logics : latest_changes, profile, etc.

"""

from ludobox.content import get_content_index
from ludobox.utils import get_resource_slug

def get_latest_changes(user=None, time=None):
    """
    Return all latest changes made on files.
    Filter is based on 2 params :
    - user
    - time
    """

    if time is not None:
        raise NotImplementedError("Filtering by time is not supported yet.")
    contents = get_content_index(short=False)

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
            if event["user"] == user:
                lastest_changes.append(
                    {
                        "title" : title,
                        "event" : event,
                        "slug" : slug
                    }
                )

    return lastest_changes
