#!/usr/bin/env python

"""
A View is an HTML rendering of a page.
"""

import util


class View:

    def __init__ (self, html_file):
        self.html_file = html_file

    def render (self):
        util.print_status_ok()
        util.print_html_header()
        with open (self.html_file) as f:
            print (f.read())
