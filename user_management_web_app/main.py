#!/usr/bin/env python

"""
Main web app server functionality.
"""

# DEBUG MODE - Remove this crap in the final thingy
import cgitb
cgitb.enable()


# Print headers
print ("Content-Type: text/html\n")

# Connect to DB

# Print some crap
print(b"""
<html>
    <body>
        <h1>Yo Dis a Lil' Stupid Site</h1>
        <p>Da purpose dis website to give you locations iz amazing.</p>
    </body>
</html>
""")
