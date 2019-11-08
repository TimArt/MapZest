#!/usr/bin/env python

"""
A View is an HTML rendering of a page.
"""

class View:

    def __init__ (self, html_file):
        self.html_file = html_file

    def get (self):
        # util.print_status_ok()
        # util.print_html_header()
        file_content = ''
        with open (self.html_file) as f:
            file_content = f.read()
        return file_content
