#!/usr/bin/env python3

import sys, time, math, pprint, twitter, spotipy
import datetime, traceback
import spotipy.util as util

sys.path.append('../')
from env import env as enviorn
from twitter_functions import twitter_functions as twitfunc

# Verifing valid log file
try:
    testfile = open(sys.argv[1],"r")
except IOError:
    print("Invalid Log File!\n Usage: ./app.py <logfile>")
    raise

testfile.close()

# Functions

def grabFromPayload(results):
    return results["item"]["name"], results["item"]["external_urls"]["spotify"], results["progress_ms"], results["item"]["duration_ms"], results["item"]["uri"]

def mainLoop():

    # Creates an Authentication object that has all of the keys for twitter and spotify
    e = enviorn()
    tf = twitfunc()

    cur_tr_uri = str()
    prev_tr_uri = str()

    while True:

        slp_time = 0
        hwp = 0

        # Twitter Authentication
        twit = twitter.Api(consumer_key=e.twit_consumer_key,
                            consumer_secret=e.twit_consumer_secret,
                            access_token_key=e.twit_access_token_key,
                            access_token_secret=e.twit_access_token_secret)

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

                # Grab relavent information from the payload if there are results
                if(results != None):

                    artist_query = []
                    tr_name, tr_link, cur_tr_prog, tr_len, cur_tr_uri = grabFromPayload(results)

                    # Fetching the Artists in on the song and putting them into a list
                    num_artists = len(results["item"]["artists"])

                    for i in range(num_artists):
                        artist_query.append(results["item"]["artists"][i]["name"])

                    # If the song is currently playing, its been playing for longer than
                    # half of its duration, and its not the previous track, then Tweet it out
                    if (results["is_playing"] and
                        tr_len/2 < cur_tr_prog and
                        cur_tr_uri != prev_tr_uri):

                        # Catching Twitter Error
                        try:
                            tr_artist = tf.lookup_user(twit = twit, query = artist_query)
                            status = twit.PostUpdate("Current Track: " + tr_name + "\nArtists: " + tr_artist + "\nListen now at: " + tr_link)
                            # pprint.pprint(results["item"]["artists"][0])
                            print(status)
                            with open(sys.argv[1], "a") as log:
                                log.write("Sucessful Tweet!\n")
                                log.write(str(status) + "\n")
                                log.write("--------------------------------------------------------------------------\n")
                            prev_tr_uri = cur_tr_uri

                        except twitter.error.TwitterError as err:
                            print("This song has already been tweeted!\n" + repr(err))

                        except twitfunc.InvalidTwitterAuthError as err:
                            print(err)

                        slp_time = (tr_len - cur_tr_prog) / 1000
                        slp_time = math.ceil(slp_time)
                        print("Sleeping for {} seconds!".format(slp_time))
                        time.sleep(slp_time)

                    # If the song is not playing then inform the client console
                    elif (results["is_playing"] == False):
                        print("Not currently playing anything!")
                        print("Sleeping for 20 seconds!")
                        time.sleep(20)

                    # If the current song uri is equal to the previous song uri, then
                    # Inform the client console
                    elif (cur_tr_uri == prev_tr_uri):
                        print("The current song is still the previous song!")
                        slp_time = (tr_len - cur_tr_prog) / 1000
                        if slp_time < 1:
                            slp_time = 2

                        slp_time = math.ceil(slp_time)
                        print("Sleeping for {} seconds!".format(slp_time))
                        time.sleep(slp_time)

                    # Otherwise, inform the client console that the user hasn't listened
                    # to at least half of the song.
                    else:
                        print("Have not listened to enough of the song!")
                        hwp = (3 * tr_len)/4
                        slp_time = (hwp - cur_tr_prog) / 1000
                        slp_time = math.ceil(slp_time)
                        print("Sleeping for {} seconds!".format(slp_time))
                        time.sleep(slp_time)

                else:
                    print("No user currently logged in, sleeping for 60 seconds!")
                    time.sleep(60)

        # Otherwise authentication failed and we will kill the program
        else:
            print ("Can't get token for " + username)
            exit()

try:
    mainLoop()
except Exception as e:
    with open(sys.argv[1], "a") as log:
        currTime = datetime.datetimen.now()
        tb = sys.exe_info()
        log.write("[{}]An Error has occured!: {}\n".format(str(currTime), repr(e)))
        traceback.print_tb(tb[2], file=log)
        log.write("--------------------------END LOGFILE--------------------------\n")
        raise
