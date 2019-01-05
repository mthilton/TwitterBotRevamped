#!/usr/bin/env python3

import sys
import twitter

sys.path.append('../')
from env import env as enviorn

# Creates an Authentication object that has all of the keys for twitter and spotify
e = enviorn()

# initalizing Twiter access
twit = twitter.Api(consumer_key=e.twit_consumer_key,
                  consumer_secret=e.twit_consumer_secret,
                  access_token_key=e.twit_access_token_key,
                  access_token_secret=e.twit_access_token_secret)




class twitter_functions:

    # Error that can be raised by a function in this class. If raised, the function does not have
    # any authentication passed to it
    class InvalidTwitterAuthError(Exception):
        pass

    # Looks up a user on twitter. The desired user or users are the artists of the current song
    # we are listening to. If in the first five results, there is a verified match, then
    # we will use that instead of just the name.
    def lookup_user(self, query = [], *args, twit=None):

        # Checks to see if we have auth
        if twit == None:
            raise InvalidTwitterAuthError("lookup_user Error: Requires a valid Twitter Authentication")

        # Function Vars
        final_string = ""
        twitterHandles = {}

        # For every string in the query list send a search request to twitter
        # It will search for users based on the passed string.
        for artist in query:
            query_results = twit.GetUsersSearch(term=artist,
                                                count=5)

            # Next we add the key to the dictionary with no value.
            twitterHandles[artist] = None

            # Next we check the results; if there is not a verified user in
            # those five results then we just leave the dictionary set to None
            # if there is a verified user, then we get their screen name,
            # and update the key in the dictionary. Instead of having no value
            # it now has the value of their unique twitter handle.
            for twitUser in query_results:
                if(twitUser.verified):
                    twitterHandles[artist] = "@" + twitUser.screen_name
                    break


        # finally we go though the entire dictionary. If the give key has a value,
        # add that value to the return string, otherwise just add the query string
        # to the return string.
        for i in range(len(query)):
            if i == len(query) - 1:
                if twitterHandles[query[i]] != None:
                    final_string += twitterHandles[query[i]]
                else:
                    final_string += query[i]

            else:
                if twitterHandles[query[i]] != None:
                    final_string += twitterHandles[query[i]] + ", "
                else:
                    final_string += query[i] + ", "

        return final_string
