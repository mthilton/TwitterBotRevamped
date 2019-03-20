#!/usr/bin/env python3

import sys, time, twitter, spotipy
import datetime, traceback
import spotipy.util as util

sys.path.append('../')
from sp_utils import *
<<<<<<< HEAD
from env import env
=======
from env import env as enviorn
>>>>>>> 196348e9344dad87f3c2695a7f2b2e41d804220d
from twitter_functions import twitter_functions as twitfunc

# Functions

<<<<<<< HEAD
# Gets the current time
def get_curr_time():
    t = datetime.datetime.now()
    return t.strftime("%Y-%m-%d-%X")

# Prints information about the current state to terminal if required
def check_printed(printed, state, format = None):

    state_strings = [
        "Placeholder",
        "[{}] No user currently logged in, sleeping until somebody logs in!",
        "[{}] Have not listened to enough of the song!",
        "--------------------------------------------------------------------------\n\033[32mSucessful Tweet!\u001b[0m\n{}--------------------------------------------------------------------------",
        "[{}] The current song is still the previous song!",
        "[{}] Not currently playing anything, waiting for playback to resume!"
    ]

    if not printed:
        if state != 3:
            print(state_strings[state].format(get_curr_time()))

        else:
            print(state_strings[state].format(format))

# Tweets the current song if able too. Also searches for varified artists' twitter handles on twitter
def tweet_song(sp, tf, twit, state):
    try:
        tr_artist = tf.lookup_user(twit = twit, query = sp.ct_artists_list)
        status = twit.PostUpdate("Current Track: " + sp.ct_name + "\nArtists: " + sp.ct_artists + "\nListen now at: " + sp.ct_url)
        tweet_info = str("\033[34mTweet: \u001b[0m\n" + status.text + "\n\033[33mTweet ID: \u001b[0m" + status.id_str + "\n\033[31mTimestamp: \u001b[0m" + status.created_at + "\n")
        check_printed(False, state, tweet_info)
        with open(sys.argv[1], "a") as log:
            log.write("---------------------------------------------------------------------------\n")
            log.write("Sucessful Tweet!\n")
            log.write(tweet_info)
        sp.ct_artists_list = []
        sp.tweeted = True

    except twitter.error.TwitterError as err:
        print("This song has already been tweeted!\n" + repr(err))

    except twitfunc.InvalidTwitterAuthError as err:
        print(err)

# Infinite loop that Initalizing everything, including state machine
=======
def calcSleep(env, sp, slp_time, ptu):

    # Check For valid Spotify results
    sp.update_obj(env)
    past_hwp = False

    if sp.sp_obj is None:
        return slp_time, ptu

    if ptu == "":
        ptu = sp.ct_uri

    # If we have valid results then try to acuratly calculate the sleep time

    # If the track is paused but the song is still the same song, then set sleep to 0
    # and alert the calling function
    if not sp.ct_is_playing and sp.ct_uri == ptu:
        print("Playback Paused!")
        past_hwp = True
        sp.tweeted = False
        slp_time = 0

    # If we are not still listening to the previous song then tell the calling function
    # by setting sleep time to 0, forcing it to re analyze current song.
    elif sp.ct_uri != ptu:
        print("Awoken Early!")
        ptu = sp.ct_uri
        sp.tweeted = False
        past_hwp = True
        slp_time = 0

    # If we are listening to the previous song, then check to see if there is
    # still at least 10 seconds of playback time
    else:

        hwp = (3*sp.ct_length)/4

        if not sp.tweeted:
            # If there is more than 10 seconds of playback time then sleep for 10 seconds
            if slp_time > 10 and slp_time + sp.ct_progress < hwp:
                time.sleep(10)
                sp.update_obj(env)
                slp_time = (hwp - sp.ct_progress) / 1000
                slp_time = math.ceil(slp_time)
                past_hwp = False

            elif slp_time + sp.ct_progress > hwp:
                slp_time = 0
                past_hwp = True

        else:
            time.sleep(10)
            sp.update_obj(env)
            slp_time = (sp.ct_length - sp.ct_progress) / 1000
            slp_time = math.ceil(slp_time)
            past_hwp = True

    return slp_time, ptu, past_hwp

>>>>>>> 196348e9344dad87f3c2695a7f2b2e41d804220d
def mainLoop():

    # Setting up Enviornment IE: Keys, and needed objs
    e = env()
    tf = twitfunc()
<<<<<<< HEAD
    sp = spot(e)
=======
    sp = spot(env)

>>>>>>> 196348e9344dad87f3c2695a7f2b2e41d804220d
    prev_tr_uri = str()
    state = 1
    printed = False

    # This is the main loop that the program will run.
    # States and their associated value:
    #
    # no_user = 1
    # prog_lt_tqp = 2
    # tweet_song = 3
    # prog_gt_tqp = 4
    # wait_for_resume = 5
    while True:

        # Twitter Authentication
        twit = twitter.Api(consumer_key=e.twit_consumer_key,
                            consumer_secret=e.twit_consumer_secret,
                            access_token_key=e.twit_access_token_key,
                            access_token_secret=e.twit_access_token_secret)

        # Spotify Authentication
<<<<<<< HEAD
        sp.update_obj(e)

        # No User
        if state == 1:
            if sp.sp_obj is not None:
                if not sp.ct_is_playing:
                    state = 5
                    printed = False

                else:
                    state = 2
                    printed = False
            else:
                check_printed(printed, state)
                state = 1
                printed = True

        # Progress < 3/4 track Lenght
        elif state == 2 and sp.sp_obj is not None:
            if not sp.ct_is_playing:
                state = 5
                printed = False

            elif (sp.ct_is_playing and
                 (3*sp.ct_length)/4 < sp.ct_progress and
                 not sp.tweeted and
                 sp.ct_uri == prev_tr_uri):
                state = 3
                printed = False

            else:
                # If the song is different from the previous song, then set tweeted to false
                if sp.ct_uri != prev_tr_uri:
                    sp.tweeted = False

                prev_tr_uri = sp.ct_uri
                check_printed(printed, state)
                state = 2
                printed = True

        # Tweet Song
        elif state == 3 and sp.sp_obj is not None:
            tweet_song(sp, tf, twit, state) # Placeholder for now
            prev_tr_uri = sp.ct_uri
            state = 4
            printed = False

        # Progress > 3/4 track length && Tweeted
        elif state == 4 and sp.sp_obj is not None:
            if not sp.ct_is_playing:
                state = 5
                printed = False

            elif sp.ct_uri != prev_tr_uri:
                state = 2
                printed = False
                sp.tweeted = False

            else:
                check_printed(printed, state)
                state =  4
                printed = True

        # Waiting for Playback to be Resumed
        elif state == 5 and sp.sp_obj is not None:
            if sp.ct_is_playing:
                if sp.tweeted:
                    state  = 4
                    printed = False

                else:
                    state = 2
                    printed = False

            else:
                check_printed(printed, state)
                state = 5
                printed = True
=======
        sp.update_obj(env)

        # Grab relavent information from the payload if there are results
        if sp.sp_obj is not None:

            # If the song is currently playing, its been playing for longer than
            # half of its duration, and its not the previous track, then Tweet it out
            if sp.ct_is_playing and (3*sp.ct_length)/4 < sp.ct_progress and not sp.tweeted and sp.ct_uri == prev_tr_uri:

                # Catching Twitter Error
                try:
                    tr_artist = tf.lookup_user(twit = twit, query = sp.ct_artists_list)
                    status = twit.PostUpdate("Current Track: " + sp.ct_name + "\nArtists: " + sp.ct_artists + "\nListen now at: " + sp.ct_url)
                    tweet_info = str("\033[34mTweet: \u001b[0m\n" + status.text + "\n\033[33mTweet ID: \u001b[0m" + status.id_str + "\n\033[31mTimestamp: \u001b[0m" + status.created_at + "\n")
                    print( "--------------------------------------------------------------------------\n\033[32mSucessful Tweet!\u001b[0m\n" + tweet_info + "--------------------------------------------------------------------------")
                    with open(sys.argv[1], "a") as log:
                        log.write("---------------------------------------------------------------------------\n")
                        log.write("Sucessful Tweet!\n")
                        log.write(tweet_info)
                    prev_tr_uri = sp.ct_uri
                    sp.ct_artists_list = []
                    sp.tweeted = True

                except twitter.error.TwitterError as err:
                    print("This song has already been tweeted!\n" + repr(err))

                except twitfunc.InvalidTwitterAuthError as err:
                    print(err)

            # If the song is not playing then inform the client console
            elif not sp.ct_is_playing:
                currTime = datetime.datetime.now()
                currTime = currTime.strftime("%Y-%m-%d-%X")
                print("[{}] Not currently playing anything, waiting for playback to resume!".format(str(currTime)))
                while not sp.ct_is_playing:
                    time.sleep(10)
                    sp.update_obj(env)
                    if sp.sp_obj is None:
                        break

            # If the current song uri is equal to the previous song uri, then
            # Inform the client console
            elif sp.ct_uri == prev_tr_uri:
                currTime = datetime.datetime.now()
                currTime = currTime.strftime("%Y-%m-%d-%X")
                print("[{}] The current song is still the previous song!".format(str(currTime)))
                slp_time = (sp.ct_length - sp.ct_progress) / 1000

                slp_time = math.ceil(slp_time)
                print("   Sleeping for {} seconds!".format(slp_time))
                if not sp.tweeted:
                    while slp_time > 0:
                        slp_time, ptu, past = calcSleep(env, sp, slp_time, ptu)
                    sp.tweeted = False
                else:
                    while slp_time > 0:
                        slp_time, ptu, past = calcSleep(env, sp, slp_time, ptu)
                    sp.tweeted = True
                ptu = ""

            # Otherwise, inform the client console that the user hasn't listened
            # to at least half of the song.
            else:
                prev_tr_uri = sp.ct_uri
                sp.tweeted = False
                currTime = datetime.datetime.now()
                currTime = currTime.strftime("%Y-%m-%d-%X")
                print("[{}] Have not listened to enough of the song!".format(str(currTime)))
                hwp = (3 * sp.ct_length)/4
                slp_time = (hwp - sp.ct_progress) / 1000
                slp_time = math.ceil(slp_time)
                print("   Sleeping for {} seconds!".format(slp_time))
                past = False
                while not past:
                    slp_time, ptu, past = calcSleep(env, sp, slp_time, ptu)
                ptu = ""
>>>>>>> 196348e9344dad87f3c2695a7f2b2e41d804220d

        # Correction for falling out of state, (Not State 1 but also sp_obj is None)
        # Essentially resetting to the default state
        else:
<<<<<<< HEAD
            state = 1
            printed = False

        # Add a sleep(5) as to not spam either Api
        time.sleep(5)

# Verifing valid log file
try:
    testfile = open(sys.argv[1],"r")
except IOError:
    print("Invalid Log File!\nUsage: ./app.py <logfile>")
    raise

testfile.close()
=======
            currTime = datetime.datetime.now()
            currTime = currTime.strftime("%Y-%m-%d-%X")
            print("[{}] No user currently logged in, sleeping until somebody logs in!".format(str(currTime)))
            while sp.sp_obj is None:
                sp.update_obj(env)
                time.sleep(10)
>>>>>>> 196348e9344dad87f3c2695a7f2b2e41d804220d

# Enables Proper Logging of the program
try:
    mainLoop()
except Exception as e:
    with open(sys.argv[1], "a") as log:
        currTime = get_curr_time()
        tb = sys.exc_info()
        log.write("---------------------------------------------------------------------------\n")
        log.write("[{}] An Error has occured!: {}\n".format(str(currTime), repr(e)))
        traceback.print_tb(tb[2], file=log)
        log.write("--------------------------------END LOGFILE--------------------------------\n")
    raise
