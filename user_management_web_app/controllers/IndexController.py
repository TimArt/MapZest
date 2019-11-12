#!/usr/bin/env python

"""
Homepage functionality.
"""
from lib.util.util import *

class IndexController:

    def get (request):
        # If not logged in, redirect to login
        return (HTTP_STATUS_REDIRECT, [('Location', '/login')], '')
        # Else, get user information from token and display
