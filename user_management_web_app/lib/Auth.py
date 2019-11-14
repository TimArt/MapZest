#!/usr/bin/env python

from lib.Middleware import Middleware
from lib.Response import Response
from lib.Cookies import Cookies
from lib.config import *
import secrets
import hashlib
import os

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

        # GET PASSWORD SALT+HASH COMBO (could be in a single column called hash)
        # FROM the USER with user_email
        # as variable : db_hash_bytes

        # If failed authentication stop and return False
        # if not Auth.verify_password_hash (user_password, db_hash_bytes):
        #   return False

        # Otherwize continue to generate token

        # Generate authentication token
        # auth_token = secrets.token_bytes (SECURE_TOKEN_NUM_BYTES)
        auth_token = secrets.token_hex (SECURE_TOKEN_NUM_BYTES)

        # STORE AUTH TOKEN IN DB - text file is test code
        with open(AUTH_TOKEN_TEST_DB_FILE, 'w') as file:
            file.write (auth_token)

        # Store authentication token in cookie
        Cookies.set (AUTH_TOKEN_COOKIE_KEY, auth_token)

        return True


    @staticmethod
    def hash_password (password_str):
        assert (isinstance (password_str, str))

        salt = os.urandom (HASH_SALT_NUM_BYTES)
        key = hashlib.pbkdf2_hmac (HASH_ALGORITHM,
                                   password.encode (encoding=ENCODING),
                                   salt,
                                   HASH_ITERATIONS)
        return salt + key


    @staticmethod
    def verify_password_hash (password_to_verify_str, true_hash_bytes):
        assert (isinstance (password_to_verify_str, str))
        assert (isinstance (true_hash_bytes, bytes))

        true_hash_salt = true_hash[:HASH_SALT_NUM_BYTES]
        true_hash_key = true_hash[HASH_SALT_NUM_BYTES:]

        key_to_verify = hashlib.pbkdf2_hmac (HASH_ALGORITHM,
                                             password_to_verify.encode (encoding=ENCODING),
                                             true_hash_salt,
                                             HASH_ITERATIONS)

        return true_hash_key == key_to_verify
