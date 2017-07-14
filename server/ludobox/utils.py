#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from datetime import datetime
from jsonpatch import JsonPatch
from slugify import slugify

regex_url = re.compile(
    r'^(?:http|ftp)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def validate_url(url):
    """Returns True if the URL is valid"""
    if regex_url.match(url) is not None : return True

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    elif isinstance(obj, JsonPatch):
        serial = list(obj)
        return serial
    # raise TypeError ("Type not serializable")

def get_resource_slug(data):
    """Get the slugified name of the game based on the data set"""
    try:
        slug = slugify(data["title"])
        # add language
        language = data["audience"]["language"]
        return "%s-%s"%(slug,language)
    except KeyError as e:
        # TODO more explicit error message
        message = "KeyError occured while "\
                  "writing game info file to path '{path}'. "\
                  "Impossible to access data['title'].".format(
                    path=data)
        raise LudoboxError(message)
