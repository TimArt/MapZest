#!/usr/bin/env python

from http import cookies

class Cookies:
    """
    A global singleton class allowing for getting and setting cookies. Every
    HTTP request should call init_session_cookies to grab the currently
    available cookies and every HTTP reply should send any cookies added to this
    singleton class.
    """
    cookies_kv = cookies.SimpleCookie() # Initialized at app startup

    @classmethod
    def init (cls, environ):
        cls.cookies_kv.load (environ.get ('HTTP_COOKIE', ''))

    @classmethod
    def get (cls, cookie_key):
        """
        @return string cookie value for key or empty string if key not found
        """
        morsel = cls.cookies_kv.get (cookie_key)
        return "" if morsel is None else morsel.value

    @classmethod
    def set (cls, key, value):
        """
        Sets a cookie key and value.
        """
        cls.cookies_kv[key] = value

    @classmethod
    def getAll (cls):
        return cls.cookies_kv
