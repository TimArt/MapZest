#!/usr/bin/env python

"""
Main web app user management server functionality.
This is meant to be used with the Apache module mod_wsgi to run.

For testing launch with:
    mod_wsgi-express start-server <THIS FILE'S NAME>
"""

import importlib
from lib.Route import Route   # Our custom framework library
from lib.View import View    # Our custom framework library
from lib.util.util import *
from routes import *    # Website routes

import cgitb  # CGI Traceback Manager in Browser
cgitb.enable()


def application (environ, start_response):
    """
    Main WSGI Application
    Based on input from `environ` about the HTTP request, we react by attempting
    to route the request via the `attemptRoute` function. We then output the
    associated HTTP Headers and return the content as a byte list.

    @param enciron: environment variables such as request method
    @param start_response: method to output HTTP status and headers
    """
    status_http, output_html = attemptRoute (environ)

    # Debug Output String
    outputString = f'{output_html}\n\n\n{environ}'

    outputBytes = outputString.encode (encoding='UTF-8', errors='strict')
    response_headers = [('Content-type', 'text/html'),
                        ('Content-Length', str(len(outputBytes)))]

    # Send HTTP Headers
    start_response (status_http, response_headers)

    # Send Page Content as byte list
    return [outputBytes]


def attemptRoute (environ):
    """
    Attempts running a route based on environ input of HTTP request content.

    @return (status, htmlOutput): a tuple containing the HTTP Status string and
                                  an HTML output string
    """
    REQUEST_METHOD = environ['REQUEST_METHOD']
    REQUEST_URI = environ['REQUEST_URI']

    # Route request to correct page script handler
    try:
        route_dest = Route.getDestination (REQUEST_METHOD, REQUEST_URI)
        is_view = False
        view_file = ''
        controller_file = ''

        if type (route_dest) is tuple:
            if route_dest[0] == "view":
                is_view = True
                view_file = route_dest[1]
            else:
                controller_file = route_dest[1]
        else:
            controller_file = route_dest


        # Return View
        if is_view:
            # Render HTML
            view = View ("views/" + view_file)
            return (HTTP_STATUS_OK, view.get())
        else: # Run controller file
            # mod = importlib.import_module (controller_file)
            # mod.HelloWorld()
            return (HTTP_STATUS_NOT_FOUND, HTTP_STATUS_NOT_FOUND_HTML)

    except UndefinedRouteError:
        return (HTTP_STATUS_NOT_FOUND, HTTP_STATUS_NOT_FOUND_HTML)



# Setup Debug Error Catching Middleware - setup config for this
# from paste.exceptions.errormiddleware import ErrorMiddleware
# application = ErrorMiddleware(application, debug=True)
