#!/usr/bin/env python

"""
Main web app user management server functionality.
This is meant to be used with the Apache module mod_wsgi to run.

For testing launch with:
    mod_wsgi-express start-server <THIS FILE'S NAME>
"""

from lib.Route import Route   # Our custom framework library
from lib.View import View    # Our custom framework library
from lib.Response import *
from lib.Cookies import Cookies
from routes import *    # Website routes
from cgi import parse_qs, escape

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
    Cookies.init (environ)

    response = attemptRoute (environ)

    # Debug Output String
    outputString = f'{response.output_html}\n\n\n<h1>DEBUG</h1>\n<h2>Eniron:</h2>\n{environ}\n<h2>Cookies:</h2>\n{Cookies.getAll()}'
    # outputString = f'{output_html}'
    outputBytes = outputString.encode (encoding='UTF-8', errors='strict')


    response_headers = [('Content-type', 'text/html'),
                        ('Content-Length', str (len (outputBytes)))]

    for header in response.headers_http:
        response_headers.append (header)

    # Send HTTP Headers
    start_response (response.status_http, response_headers)

    # Send Page Content as byte list
    return [outputBytes]


def attemptRoute (environ):
    """
    Attempts running a route based on environ input of HTTP request content.

    @return Response: an HTTP response
    """
    REQUEST_METHOD = environ['REQUEST_METHOD']
    REQUEST_URI = environ['REQUEST_URI']

    # Route request to correct page script handler
    try:
        route_dest = Route.getDestination (REQUEST_METHOD, REQUEST_URI)
        is_view = False
        view_file = ''
        controller_cmd = ''
        middleware_cmd_list = []

        assert (isinstance (route_dest), tuple)

        if isinstance (route_dest[0], str):
            is_view = True
            view_file = route_dest[0]
        else:
            controller_cmd = route_dest[0]

        middleware_cmd_list = route_dest[1]

        # Run middleware before main route
        for middleware_cmd in middleware_cmd_list:
            middleware_response = middleware_cmd (environ)
            if middleware_response is not None:
                return middleware_response

        # Return view or run controller to produce HTTP response with HTML
        if is_view:
            return Response.okDisplay (View (f"views/{view_file}").get())
        else:  # Run controller file
            return controller_cmd (parse_request (environ))

    except UndefinedRouteError:
        return Response.notFound404Error()


def parse_request (environ):
    """
    Parses user post input of the HTTP request.
    """
    # environ variable CONTENT_LENGTH may be empty or missing
    try:
        request_body_size = int (environ.get ('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0

    # When the method is POST the variable will be sent
    # in the HTTP request body which is passed by the WSGI server
    # in the file like wsgi.input environment variable.
    request_body = environ['wsgi.input'].read (request_body_size)
    request_dict = parse_qs (request_body.decode())

    # Escape user input
    for key, valList in request_dict.items():
        for val in valList:
            val = escape (val)

    return request_dict


# Setup Debug Error Catching Middleware - setup config for this
# from paste.exceptions.errormiddleware import ErrorMiddleware
# application = ErrorMiddleware(application, debug=True)
