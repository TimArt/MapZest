#!/usr/bin/env python

from lib.Response import Response
from lib.View import View


class IndexController:
    """
    Manages homepage account display.
    """

    @staticmethod
    def get (request):
        # GET FRIEND REQUESTS FROM DB
        friend_requests = ['timarterbury@gmail.com', 'yomamma@yomamma.com',
                           'Idunno@whatever.com', 'heyheyhey@mmmk.org']

        # GET FRIEND LIST AND LOCATIONS FROM DB
        friend_list = {
                        'joebob@qwert.poo':
                            {
                                'latitude': '8393.53324',
                                'longitude': '3920134.4'
                            },
                            'another@wut.omg':
                            {
                                'latitude': '74344.44',
                                'longitude': '32442.4'
                            },
                            'swagdank@wwww.com':
                            {
                                'latitude': '74344.44',
                                'longitude': '32442.4'
                            }
                        }

        # GET USER LIST AND LOCATIONS FROM DB
        user_list = ['wut', 'hey', 'omg', 'okay']

        friend_request_html = View ("views/friend-request.html").get()
        friend_list_html = View ("views/friend-list.html").get()
        user_list_html = View ("views/user-list.html").get()

        friend_list_html_filled = []
        for user_email, location in friend_list.items():
            friend_list_html_filled.append (
                friend_list_html.format (user_email=user_email,
                                         latitude=location['latitude'],
                                         longitude=location['longitude']))

        main_page = View (f"views/index.html").get()
        main_page = main_page.format (user_email=user_email,
                        friend_requests=''.join (map (friend_request_html.format, friend_requests)),
                        friend_list=''.join (friend_list_html_filled),
                        user_list=''.join (map (user_list_html.format, user_list)))

        return Response.okDisplay (main_page)
