#!/usr/bin/env python3

import sys
import spotipy
import spotipy.util as util
import twitter
import time

sys.path.append('../')
from env import env as enviorn

# Creates an Authentication object that has all of the keys for twitter and spotify
e = enviorn()

# initalizing Twiter access
twit = twitter.Api(consumer_key=e.twit_consumer_key,
                  consumer_secret=e.twit_consumer_secret,
                  access_token_key=e.twit_access_token_key,
                  access_token_secret=e.twit_access_token_secret)

cur_tr_uri = str()
prev_tr_uri = str()

while True:

    slp_time = 0
    hwp = 0

    # Spotify Authentication
    scope = 'user-read-currently-playing'
    token = util.prompt_for_user_token(username=e.spot_username,
                                        scope=scope,
                                        client_id=e.spot_client_id,
                                        client_secret= e.spot_client_secret,
                                        redirect_uri=e.spot_redirect_uri)

    # On success grab the current user playing track
    if token:

            sp = spotipy.Spotify(auth=token)

            results = sp.current_user_playing_track()

            # Grab relavent information form the payload
            tr_name = results["item"]["name"]
            tr_link = results["item"]["external_urls"]["spotify"]
            cur_tr_prog = results["progress_ms"]
            tr_len = results["item"]["duration_ms"]
            cur_tr_uri = results["item"]["uri"]

            # Fetching the Artists in on the song and concating them to a string
            num_artists = len(results["item"]["artists"])

            # If there are more than one artist then run a for loop
            if num_artists > 1:
                tr_artist = results["item"]["artists"][0]["name"] + ", "

                for a in results["item"]["artists"][1:num_artists-2]:
                    tr_artist += a["name"] + ", "

                tr_artist += "and " + results["item"]["artists"][num_artists-1]["name"]

            # Otherwise just grab the artist string from the payload
            else:
                tr_artist = results["item"]["artists"][0]["name"]

            # If the song is currently playing, its been playing for longer than
            # half of its duration, and its not the previous track, then Tweet it out
            if (results["is_playing"] and
                tr_len/2 < cur_tr_prog and
                cur_tr_uri != prev_tr_uri):

                # Catching Twitter Error
                try:
                    status = twit.PostUpdate("Current Track: " + tr_name + "\nArtists: " + tr_artist + "\nListen now at: " + tr_link)
                    print(status)
                    prev_tr_uri = cur_tr_uri
                except twitter.error.TwitterError as err:
                    print("This song has already been tweeted!\n" + repr(err))

                slp_time = (tr_len - cur_tr_prog) / 1000
                time.sleep(slp_time)

            # If the song is not playing then inform the client console
            elif (results["is_playing"] == False):
                print("Not currently playing anything!")
                time.sleep(20)

            # If the current song uri is equal to the previous song uri, then
            # Inform the client console
            elif (cur_tr_uri == prev_tr_uri):
                print("The current song is still the previous song!")
                slp_time = (tr_len - cur_tr_prog) / 1000
                print("Sleeping for {} seconds!".format(slp_time))
                time.sleep(slp_time)

            # Otherwise, inform the client console that the user hasn't listened
            # to at least half of the song.
            else:
                print("Have not listened to enough of the song!")
                hwp = tr_len/2
                slp_time = (hwp - cur_tr_prog) / 1000
                print("Sleeping for {} seconds!".format(slp_time))
                time.sleep(slp_time)

    # Otherwise authentication failed and we will kill the program
    else:
        print ("Can't get token for " + username)
        exit()
