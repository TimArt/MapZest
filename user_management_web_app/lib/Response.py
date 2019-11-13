#!/usr/bin/env python

HTTP_STATUS_OK = '200 OK'
HTTP_STATUS_REDIRECT = '303 See Other'
HTTP_STATUS_NOT_FOUND = '404 Not Found'


class Response:
    """
    An HTTP Response to the client.
    """
    status_http = ''
    output_html = ''
    headers_http = []

    def __init__ (self, status_http, output_html, added_headers=[]):
        assert (isinstance (status_http, str))
        assert (isinstance (added_headers, list))
        for header in added_headers:
            assert (isinstance (header, tuple))
            for item in header:
                assert (isinstance (item, str))
        assert (isinstance (output_html, str))

        self.status_http = status_http
        self.added_headers = added_headers
        self.output_html = output_html

    @classmethod
    def okDisplay (cls, output_html):
        """
        Factory method to construct a Response for an HTTP OK status page display.
        """
        assert (isinstance (output_html, str))
        return cls (HTTP_STATUS_OK, output_html)

    @classmethod
    def redirect (cls, url_path):
        """
        Factory method to construct a Response for a redirect.
        """
        assert (isinstance (url_path, str))
        return cls (HTTP_STATUS_REDIRECT, '', [('Location', url_path)])

    @classmethod
    def notFound404Error (cls):
        """
        Factory method to construct a Response for a 404 error.
        """
        return cls (HTTP_STATUS_NOT_FOUND,
                    '<h1>404 Error : Some crap went down, so just <a href="/">HEAD HOME</a>.</h1>',
                    [])
