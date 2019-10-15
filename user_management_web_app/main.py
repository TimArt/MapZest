#!/usr/bin/env python

"""
Main web app server functionality.
"""

# DEBUG MODE - Remove this crap in the final thingy
#import cgitb
#cgitb.enable()

import util

util.print_header()

# Connect to DB

# Check url & token
# If authenticated:
#   show content
# Else display unauthorized or redirect to login

with open('views/login.html') as f:
    print (f.read())
