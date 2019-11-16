#!/usr/bin/env python

from lib.Middleware import Middleware
from lib.Response import Response
from lib.Cookies import Cookies
from lib.config import *
import secrets
import hashlib
import os
import psycopg2  # Postgres Connection

# DEBUG STUFF
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
        cookie_token = Cookies.get (AUTH_TOKEN_COOKIE_KEY)

        with psycopg2.connect (POSTGRES_DB_CONNECT) as conn:
            with conn.cursor() as curs:
                curs.execute ("SELECT does_user_auth_token_exist (%s, %s)",
                              (User.email, cookie_token))
                does_valid_token_exist = curs.fetchone()[0]

        return does_valid_token_exist



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
        auth_token = secrets.token_bytes (SECURE_TOKEN_NUM_BYTES)

        with psycopg2.connect (POSTGRES_DB_CONNECT) as conn:
            with conn.cursor() as curs:
                curs.execute ("CALL create_user_auth_token (%s, %s)",
                              (User.email, auth_token))

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
