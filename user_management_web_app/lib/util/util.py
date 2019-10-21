#!/usr/bin/env python

"""
Utility functions.
"""

import os
import sys


def print_status_ok():
    print ("Status: 200 OK")


def print_html_header():
    print ("Content-Type: text/html\n")


def print_debug_version_and_env():
    print ("<table>")
    print ("<tr><td>Python Version</td><td>" + sys.version + "</td></tr>")

    for param in os.environ.keys():
        # Python 3: print (f"<tr><td>{param}</td><td>{os.environ.keys(param)}</td></tr>")
        print ("<tr><td>" + param + "</td><td>" + os.environ[param] + "</td></tr>")
    print ("</table>")


def print_error():
    print ("Status: 404 Not Found")
    print_html_header()
    print ('<h1>404 Error : Some crap went down, so just <a href="/">HEAD HOME</a>.</h1>')
