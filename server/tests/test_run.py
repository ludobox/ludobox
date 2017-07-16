#!/usr/bin/env python
# -*- coding: utf-8 -*-

from LudoboxTestCase import LudoboxTestCase
from ludobox.run import get_server_port

class TestLudoboxRunServer(LudoboxTestCase):

    def test_get_server_port(self):
        """Test default and custom port for server"""
        self.assertEquals(get_server_port(None), 8080)
        self.assertEquals(get_server_port(4040), 4040)
