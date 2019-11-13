#!/usr/bin/env python

"""
Login functionality.
"""
from lib.util.util import *
from lib.Cookies import Cookies

class LoginController:

    def login (request):
        email = request.get ('email', [''])[0]  # Returns the first email value.
        password = request.get ('password', [''])[0]

        is_authenticated = False
        # CHECK IF USERNAME AND PASSWORD HASH ARE IN THE DB
        is_authenticated = True

        # Stop if not authenticated
        if not is_authenticated:
            return (HTTP_STATUS_REDIRECT, [('Location', '/login')], '')

        # If was authenticated
        # GENERATE AND STORE AUTH TOKEN

        Cookies.set ('auth_token', 'AUTH_TOKEN_TEST_YO')

        return (HTTP_STATUS_REDIRECT, [('Location', '/')], '') # Redirect home
