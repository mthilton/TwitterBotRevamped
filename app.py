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
    print("Invalid Log File!\nUsage: ./app.py <logfile>")
    raise

testfile.close()

# Functions

def grabFromPayload(results):

    # Check to see if results are None
    if results is None:
        return None

    # If there is proper data then return the proper information
    return results["item"]["name"], results["item"]["external_urls"]["spotify"], results["progress_ms"], results["item"]["duration_ms"], results["item"]["uri"]

def refeshSpotifyToken(env):
    scope = 'user-read-currently-playing'
    token = util.prompt_for_user_token(username=env.spot_username,
                                        scope=scope,
                                        client_id=env.spot_client_id,
                                        client_secret= env.spot_client_secret,
                                        redirect_uri=env.spot_redirect_uri)

    # On success grab the current user playing track
    if token:
        sp = spotipy.Spotify(auth=token)
        return sp.current_user_playing_track()

    # Otherwise authentication failed and we will kill the program
    else:
        print ("Can't get token for " + e.spot_username)
        exit()


def calcSleep(env, slp_time, ptu):

    results = refeshSpotifyToken(env)

    # Check For valid Spotify results
    if results is None:
        return slp_time, ptu

    tr_name, tr_link, cur_tr_prog, tr_len, cur_tr_uri = grabFromPayload(results)

    if ptu == "":
        ptu = cur_tr_uri

    # If we have valid results then try to acuratly calculate the sleep time

    # If we are listening to the previous song, then check to see if there is
    # still at least 10 seconds of playback time
    if cur_tr_uri == ptu:

        # If there is more than 10 seconds of playback time then sleep for 10 seconds
        if slp_time > 10:
            time.sleep(10)
            slp_time -= 10

        # Otherwise sleep for the remainder of the song and set sleep time to 0
        else:
            time.sleep(slp_time)
            slp_time = 0

    # If we are not still listening to the previous song then tell the calling function
    # by setting sleep time to 0, forcing it to re analyze current song.
    else:
        print("Awoken Early!\n")
        ptu = cur_tr_uri
        slp_time = 0

    return slp_time, ptu

def mainLoop():

    # Creates an Authentication object that has all of the keys for twitter and spotify
    env = enviorn()
    tf = twitfunc()

    cur_tr_uri = str()
    prev_tr_uri = str()
    ptu = str()

    while True:

        slp_time = 0
        hwp = 0

        # Twitter Authentication
        twit = twitter.Api(consumer_key=env.twit_consumer_key,
                            consumer_secret=env.twit_consumer_secret,
                            access_token_key=env.twit_access_token_key,
                            access_token_secret=env.twit_access_token_secret)

        # Spotify Authentication
        results = refeshSpotifyToken(env)

        # Grab relavent information from the payload if there are results
        if results is not None:

            artist_query = []
            tr_name, tr_link, cur_tr_prog, tr_len, cur_tr_uri = grabFromPayload(results)

            # Fetching the Artists in on the song and putting them into a list
            num_artists = len(results["item"]["artists"])

            for i in range(num_artists):
                artist_query.append(results["item"]["artists"][i]["name"])

            # If the song is currently playing, its been playing for longer than
            # half of its duration, and its not the previous track, then Tweet it out
            if (results["is_playing"] and
                (3*tr_len)/4 < cur_tr_prog and
                cur_tr_uri == prev_tr_uri):

                # Catching Twitter Error
                try:
                    tr_artist = tf.lookup_user(twit = twit, query = artist_query)
                    status = twit.PostUpdate("Current Track: " + tr_name + "\nArtists: " + tr_artist + "\nListen now at: " + tr_link)
                    tweet_info = str("Tweet: " + status.text + "\nTweet ID: " + status.id_str + "\nTimestamp: " + status.created_at + "\n")
                    print("\33[2;32;40m Sucessful Tweet!\n" + tweet_info + "--------------------------------------------------------------------------\n")
                    with open(sys.argv[1], "a") as log:
                        log.write("Sucessful Tweet!\n")
                        log.write(tweet_info)
                        log.write("--------------------------------------------------------------------------\n")
                    prev_tr_uri = cur_tr_uri

                except twitter.error.TwitterError as err:
                    print("This song has already been tweeted!\n" + repr(err))

                except twitfunc.InvalidTwitterAuthError as err:
                    print(err)

                slp_time = (tr_len - cur_tr_prog) / 1000
                slp_time = math.ceil(slp_time)
                print("Sleeping for {} seconds!".format(slp_time))
                while slp_time > 0:
                    slp_time, ptu = calcSleep(env, slp_time, ptu)
                ptu = ""

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

                slp_time = math.ceil(slp_time)
                print("Sleeping for {} seconds!".format(slp_time))
                while slp_time > 0:
                    slp_time, ptu = calcSleep(env, slp_time, ptu)
                ptu = ""

            # Otherwise, inform the client console that the user hasn't listened
            # to at least half of the song.
            else:
                prev_tr_uri = cur_tr_uri
                print("Have not listened to enough of the song!")
                hwp = (3 * tr_len)/4
                slp_time = (hwp - cur_tr_prog) / 1000
                slp_time = math.ceil(slp_time)
                print("Sleeping for {} seconds!".format(slp_time))
                while slp_time > 0:
                    slp_time, ptu = calcSleep(env, slp_time, ptu)
                ptu = ""

        else:
            print("No user currently logged in, sleeping for 60 seconds!")
            time.sleep(60)

try:
    mainLoop()
except Exception as e:
    with open(sys.argv[1], "a") as log:
        currTime = datetime.datetime.now()
        tb = sys.exc_info()
        log.write("[{}]An Error has occured!: {}\n".format(str(currTime), repr(e)))
        traceback.print_tb(tb[2], file=log)
        log.write("--------------------------END LOGFILE--------------------------\n")
    raise
