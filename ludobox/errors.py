#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO improve this exception by always providing an advice to solve the
#   problem
# TODO improve this excetion by always providing a context ???
class LudoboxError(Exception):
    """Base class for all the custom exceptions of the module."""

    def __init__(self, message):
        """Set the message for the exception."""
        # without this you may get DeprecationWarning
        self.message = message

        # Call the base class constructor with the parameters it needs
        super(LudoboxError, self).__init__(message)
