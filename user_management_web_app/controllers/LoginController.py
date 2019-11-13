#!/usr/bin/env python

"""
Login functionality.
"""
from lib.Response import Response
from lib.Auth import Auth
from lib.View import View


class LoginController:

    @staticmethod
    def get (request):
        # If already authorized, redirect to main page
        if Auth.is_authorized():
            return Response.redirect ('/')
        else:
            return Response.okDisplay (View ('views/login.html').get())


    @staticmethod
    def post (request):
        email = request.get ('email', [''])[0]  # Returns the first email value.
        password = request.get ('password', [''])[0]

        login_success = Auth.attempt_login (email, password)

        # If was not logged in, make them login again
        if not login_success:
            return Response.redirect ('/login')

        return Response.redirect ('/')
