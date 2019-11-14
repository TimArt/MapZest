#!/usr/bin/env python

from lib.Response import Response
from lib.View import View
from enum import Enum

# In DB:
# Friends Table =========
# uid firstUser
# uid secondUser
# firstUserStatus : accept or reject
# secondUserStatus : accept or reject
# timestamp of last update
#
# Only friends if both have accepted status. Default is reject status

class FriendStatus (Enum):
    unspecified = 0
    rejected = 1
    accepted = 2


class FriendController:
    """
    Handles any friend/user management requests.
    """

    @staticmethod
    def post_add_friend (request):
        """
        Adds a friend or accepts a friend request. A positive accept action is
        made by one user for another user.
        """
        # user_email = User.email
        # other_user_email = request.get ('user_email', [''])[0]  # Returns the first email value.

        # CHECK DB FOR ENTRY WITH BOTH USERS
        # IF NO ENTRY:
        #   CREATE ENTRY WHERE user_email has FriendStatus.accepted and other
        #   FriendStatus.unspecified
        # ELSE:
        #   UPDATE ENTRY for user_email FriendStatus.accepted

        return Response.redirect ('/')


    @staticmethod
    def post_remove_friend (request):
        """
        Removes a friend or rejects a friend request. A negative reject action is
        made by one user for another user.
        """
        # user_email = User.email
        # other_user_email = request.get ('user_email', [''])[0]  # Returns the first email value.

        # CHECK DB FOR ENTRY WITH BOTH USERS
        # IF NO ENTRY:
        #   DON'T DO ANYTHING
        # ELSE:
        #   UPDATE ENTRY for user_email FriendStatus.rejected

        return Response.redirect ('/')



