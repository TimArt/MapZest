#!/usr/bin/env python

"""
Login functionality.
"""


class LoginController:

    def login (request):
        email = request.get('email', [''])[0]  # Returns the first email value.
        password = request.get('password', [''])[0]

        # IF USERNAME AND HASHED PASSWORD IN DB, THEN SET TOKEN

        # We want to redirect to home page here
        return f'<h1>{email}</h1><h1>{password}</h1>'
