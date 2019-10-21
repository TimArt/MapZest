#!/usr/bin/env python

# This is the script that works for mod_wsgi-express but I wish I could get
# mod_wsgi-express to run my thing
def application(environ, start_response):
    status = '200 OK'
    output = b'Hello World!'

    response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)


    return [output]
