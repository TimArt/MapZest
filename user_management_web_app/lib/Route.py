#!/usr/bin/env python

"""
A Route is a URL path mapping to an HTTP action (get, post),
and possibly a Controller. This is a singleton class that holds
the routing map which is intended to be defined in routes.py.
"""


class UndefinedRouteError (Exception):
    """
    Exception raised when a route is attempted to be accessed from the route_map
    but that route is not present.
    """
    pass

    def __init__ (self, http_method, url_path):
        self.http_method = http_method
        self.url_path = url_path



class Route:
    route_map = {
        "get": {},
        "post": {}
    }

    @classmethod
    def getDestination (cls, http_method, url_path):
        """
        Returns a route destination from the route_map given the http_method and
        the url_path.

        @param http_method "get" or "post"
        """
        if http_method in cls.route_map and url_path in cls.route_map[http_method]:
            return cls.route_map[http_method][url_path]
        else:
            raise UndefinedRouteError (http_method, url_path)


    @classmethod
    def get (cls, url_path, controller):
        """
        Defines an HTTP GET route at the specified `url_path` to run the
        specified `controller` code to display some dynamic View to the user.
        """
        cls.route_map["get"][url_path] = ("controller", controller)


    @classmethod
    def view (cls, url_path, view):
        """
        A shortcut method for get() which also uses an HTTP GET action but
        bypasses a controller and goes straight to displaying a view. This is
        useful for any static pages in the site.
        """
        cls.route_map["get"][url_path] = ("view", view)


    @classmethod
    def post (cls, url_path, controller):
        """
        Defines an HTTP POST action at the specified `url_path` to run the
        specified `controller` code to process POSTed user data.
        """
        cls.route_map["post"][url_path] = controller
