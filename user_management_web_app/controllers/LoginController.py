#!/usr/bin/env python

from lib.Response import Response
from lib.Auth import Auth
from lib.View import View
from lib.config import *


class LoginController:
    """
    Handles login page routes and functionality.
    """

    @staticmethod
    def get (request):
        # If already authorized, redirect to main page
        if Auth.is_authorized():
            return Response.redirect ('/')
        else:
            return Response.okDisplay (View ('views/login.html').get())


    @staticmethod
    def post_login (request):
        email = request.get ('email', [''])[0]  # Returns the first email value.
        password = request.get ('password', [''])[0]

        login_success = Auth.attempt_login (email, password)

        # If was not logged in, make them login again
        if not login_success:
            return Response.redirect ('/login')

        return Response.redirect ('/')


    @staticmethod
    def post_signup (request):
        email = request.get ('email', [''])[0]  # Returns the first email value.
        password = request.get ('password', [''])[0]

        # password_hash_bytes = Auth.hash_password (password)
        # CREATE USER IN DB with email and password_hash
        # CREATE EMAIL VERIFICATION TOKEN IN DB
        # SEND VERIFICATION EMAIL

        return Response.okDisplay (View ('views/signup.html').get().format(user_email=email))
