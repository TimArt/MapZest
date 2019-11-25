#!/usr/bin/env python

from lib.Response import Response
from lib.View import View
from lib.User import *
from lib.Cookies import Cookies


class IndexController:
    """
    Manages homepage account display.
    """

    @staticmethod
    def get (request):

        friend_requests = []
        friend_list = {}
        potential_friend_list = []

        # Get related friend data from DB
        with psycopg2.connect (POSTGRES_DB_CONNECT) as conn:
            with conn.cursor() as curs:
                try:
                    user_email = Cookies.get (User.EMAIL_COOKIE_KEY)
                    curs.execute ("SELECT get_user_friend_requests (%s)",
                                  [user_email])
                except psycopg2.Error:
                    # Debug.print (str(e))
                    pass  # Continue regardless of friending error


        # GET FRIEND REQUESTS FROM DB
        # friend_requests = ['timarterbury@gmail.com', 'yomamma@yomamma.com',
        #                    'Idunno@whatever.com', 'heyheyhey@mmmk.org']

        # # GET FRIEND LIST AND LOCATIONS FROM DB
        # friend_list = {
        #                 'joebob@qwert.poo':
        #                     {
        #                         'latitude': '8393.53324',
        #                         'longitude': '3920134.4'
        #                     },
        #                     'another@wut.omg':
        #                     {
        #                         'latitude': '74344.44',
        #                         'longitude': '32442.4'
        #                     },
        #                     'swagdank@wwww.com':
        #                     {
        #                         'latitude': '74344.44',
        #                         'longitude': '32442.4'
        #                     }
        #                 }

        # # GET USER LIST AND LOCATIONS FROM DB
        # user_list = ['wut', 'hey', 'omg', 'okay']

        friend_request_html = View ("views/friend-request.html").get()
        friend_list_html = View ("views/friend-list.html").get()
        potential_friend_list_html = View ("views/user-list.html").get()

        friend_list_html_filled = []
        for user_email, location in friend_list.items():
            friend_list_html_filled.append (
                friend_list_html.format (user_email=user_email,
                                         latitude=location['latitude'],
                                         longitude=location['longitude']))

        main_page = View (f"views/index.html").get()
        main_page = main_page.format (
            user_email=Cookies.get (User.EMAIL_COOKIE_KEY),
            friend_requests=''.join (map (friend_request_html.format, friend_requests)),
            friend_list=''.join (friend_list_html_filled),
            potential_friend_list=''.join (map (potential_friend_list_html.format, potential_friend_list))
        )

        return Response.okDisplay (main_page)
