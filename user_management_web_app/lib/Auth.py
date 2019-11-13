#!/usr/bin/env python

from lib.Middleware import Middleware
from lib.Response import Response
from lib.Cookies import Cookies
from lib.config import *
import secrets

AUTH_TOKEN_COOKIE_KEY = 'auth_token'

AUTH_TOKEN_TEST_DB_FILE = 'token.txt'


class Auth (Middleware):

    # Override of middleware run method
    @staticmethod
    def run (environ):
        """
        Checks if user is authenticated. If so, returns none, otherwise redirects
        to login.

        @return Response of None
        """
        # If not authrorized, redirect, otherwize do nothing, continue route
        response = Response.redirect ('/login')
        if Auth.is_authorized():
            response = None

        return response


    @staticmethod
    def is_authorized():
        token = ''
        # CONTACT DB AND CHECK FOR PRESENCE OF AUTH TOKEN - Test with file
        try:
            with open (AUTH_TOKEN_TEST_DB_FILE, 'r') as file:
                token = file.read()
        except FileNotFoundError:
            pass

        return Cookies.get (AUTH_TOKEN_COOKIE_KEY) == token


    @staticmethod
    def attempt_login (user_email, user_password):
        """
        Attempts a user login.

        @return true if the user gets successfully logged in, false otherwise
        """

        # HASH PASSWORD

        is_authenticated = False
        # CHECK IF USERNAME AND PASSWORD HASH ARE IN THE DB
        is_authenticated = True

        if not is_authenticated:
            return False

        # Generate authentication token
        # auth_token = secrets.token_bytes (SECURE_TOKEN_NUM_BYTES)
        auth_token = secrets.token_hex (SECURE_TOKEN_NUM_BYTES)

        # STORE AUTH TOKEN IN DB - text file is test code
        with open(AUTH_TOKEN_TEST_DB_FILE, 'w') as file:
            file.write (auth_token)

        # Store authentication token in cookie
        Cookies.set (AUTH_TOKEN_COOKIE_KEY, auth_token)

        return True
