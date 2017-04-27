#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify

# TODO improve this exception by always providing an advice to solve the
#   problem
# TODO improve this excetion by always providing a context ???
class LudoboxError(Exception):
    """Base class for all the custom exceptions of the module."""

    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        """Set the message for the exception."""
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    # Call the base class constructor with the parameters it needs
    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv
    # super(LudoboxError, self).__init__(message)
