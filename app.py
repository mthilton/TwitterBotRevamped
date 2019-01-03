#!/usr/bin/env python3

import sys
import spotipy
import spotipy.util as util
import twitter
import time

sys.path.append('../')
from env import env as enviorn

# initalizing Twiter access
e = enviorn()

twit = twitter.Api(consumer_key=e.twit_consumer_key,
                  consumer_secret=e.twit_consumer_secret,
                  access_token_key=e.twit_access_token_key,
                  access_token_secret=e.twit_access_token_secret)

# status = twit.PostUpdate('I love python-twitter!')
#
# print(status.text)

# initalizing Spotify Access
scope = 'user-read-currently-playing'
cur_tr_uri = str()
prev_tr_uri = str()

while True:

    token = util.prompt_for_user_token(username=e.spot_username,
                                        scope=scope,
                                        client_id=e.spot_client_id,
                                        client_secret= e.spot_client_secret,
                                        redirect_uri=e.spot_redirect_uri)




    # On success grab the current user playing track
    # Need to have protection against same song
    if token:

            sp = spotipy.Spotify(auth=token)

            results = sp.current_user_playing_track()

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

            # Otherwise just grab the string from the payload
            else:
                tr_artist = results["item"]["artists"][0]["name"]

            # If the song is currently playing, then print it out
            if (results["is_playing"] and
                tr_len/2 < cur_tr_prog and
                cur_tr_uri != prev_tr_uri):
                status = twit.PostUpdate("Current Track: " + tr_name + "\nArtists: " + tr_artist + "\nListen now at: " + tr_link)
                print(status)
                prev_tr_uri = cur_tr_uri
                time.sleep(20)


            elif (results["is_playing"] == False):
                print("Not currently playing anything!")
                time.sleep(20)

            else:
                print("Have not listened to enough of the song or still listening to the previous song!")
                time.sleep(20)

    else:
        print ("Can't get token for " + username)
        exit()
