#!/usr/bin/env python

"""
Utility functions.
"""

# https://httpstatuses.com/
HTTP_STATUS_OK = '200 OK'
HTTP_STATUS_NOT_FOUND = '404 Not Found'
HTTP_STATUS_NOT_FOUND_HTML = '<h1>404 Error : Some crap went down, so just <a href="/">HEAD HOME</a>.</h1>'

HTTP_STATUS_REDIRECT = '303 See Other'

# def print_debug_version_and_env():
#     print ("<table>")
#     print ("<tr><td>Python Version</td><td>" + sys.version + "</td></tr>")

#     for param in os.environ.keys():
#         # Python 3: print (f"<tr><td>{param}</td><td>{os.environ.keys(param)}</td></tr>")
#         print ("<tr><td>" + param + "</td><td>" + os.environ[param] + "</td></tr>")
#     print ("</table>")
