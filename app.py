#!/usr/bin/env python3

from sp_utils import *
import sys
import os
import time
import spotipy
import datetime
import traceback
import mysql.connector

sys.path.append('../')
# Functions


# Gets the current time
def get_curr_time():
    t = datetime.datetime.now()
    return t.strftime("%Y-%m-%d-%X")


# Prints information about the current state to terminal if required
def check_printed(printed, state, format=None):

    # List of strings to be printed to the termnal based on state of the program
    state_strings = [
        "[{}] No user currently logged in, sleeping until somebody logs in!",
        "[{}] Have not listened to enough of the song!",
        "--------------------------------------------------------------------------\n\033[32mProcessed Song!\u001b[0m\n{}--------------------------------------------------------------------------",
        "[{}] The current song is still the previous song!",
        "[{}] Not currently playing anything, waiting for playback to resume!"
    ]

    # If something needs to be printed, the print it. special case print for state 2 (process_song)
    if not printed:
        if state != 2:
            print(state_strings[state].format(get_curr_time()))

        else:
            print(state_strings[state].format(format))


# Prints the current song to terminal
def process_song(sp, state):

    song_info = str("\033[34mCurrent Track: \u001b[0m" + sp.ct_name + "\033[33m\nArtists: \u001b[0m" +
                    sp.ct_artists + "\n")
    check_printed(False, state, song_info)
    update_db(sp)


def update_db(sp):

    try:
        mydb = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            user=os.getenv('MYSQL_USER'),
            passwd=os.getenv('MYSQL_PW'),
            database=os.getenv('MYSQL_DB')
        )

        mycursor = mydb.cursor()

        # Update SpTrackInfo with track information
        sql = """INSERT INTO SpTrackInfo (tr_uri, tr_name, ar_uri, ar_name, num_artists, pop, my_pop, spot_pop, AllTime_Num_Playbacks, Weekly_Num_Playbacks) \
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) \
                 ON DUPLICATE KEY \
                 UPDATE AllTime_Num_Playbacks = AllTime_Num_Playbacks + 1, Weekly_Num_Playbacks = Weekly_Num_Playbacks + 1"""

        val = (sp.ct_uri, sp.ct_name, sp.ct_artist_uri,
               sp.ct_artists, sp.ct_num_artists, 0, 0, 0, 1, 1)
        mycursor.execute(sql, val)
        mydb.commit()
        print("Track Updater: {} records inserted into SpTrackInfo in DB TBR.".format(
            mycursor.rowcount))

        # Update popularity
        sql = """SELECT Weekly_Num_Playbacks \
            From SpTrackInfo\
            WHERE Weekly_Num_Playbacks > 0"""
        mycursor.execute(sql)
        playbacks = mycursor.fetchall()
        total_playbacks = 0
        for count in playbacks:
            total_playbacks += count[0]

        sql = """ SELECT Weekly_Num_Playbacks \
                  FROM SpTrackInfo \
                  WHERE tr_uri = '{}'"""
        mycursor.execute(sql.format(sp.ct_uri))
        track_playbacks = mycursor.fetchall()

        # Get Spotify-like popularity ratings based on my listening habbits
        my_pop = int((track_playbacks[0][0]/total_playbacks) * 1000)
        pop = (my_pop + sp.ct_popularity) // 2

        sql = """UPDATE SpTrackInfo \
                 SET pop = {}, my_pop = {}, spot_pop = {} \
                 WHERE tr_uri = '{}'"""
        mycursor.execute(sql.format(pop, my_pop, sp.ct_popularity, sp.ct_uri))
        mydb.commit()
        print("Popularity Updater: {} records inserted into SpTrackInfo in DB TBR.".format(
            mycursor.rowcount))

        # Update ArtistInfo with artist information
        sql = """INSERT INTO ArtistInfo (ar_name, ar_uri, AllTimeCount, WeeklyCount) \
                     VALUES (%s, %s, %s, %s) \
                     ON DUPLICATE KEY \
                     UPDATE AllTimeCount = AllTimeCount + 1, WeeklyCount = WeeklyCount + 1"""

        for uri, ar in sp.ct_ar_uri_dict.items():
            val = (ar, uri, 1, 1)
            mycursor.execute(sql, val)
            mydb.commit()
            print("Artist Updater: {} records inserted into SpTrackInfo in DB TBR.".format(
                mycursor.rowcount))

    except mysql.connector.Error as error:
        mydb.rollback()  # rollback if any exception occured
        print("Failed inserting record into SpTrackInfo {}".format(error))

    finally:
        # closing database connection.
        if(mydb.is_connected()):
            mycursor.close()
            mydb.close()


# Infinite loop that Initalizing everything, including state machine
def mainLoop():

    # Setting up Enviornment IE: Keys, and needed objs
    sp = spot()
    prev_tr_uri = str()
    state = 0
    printed = False
    song_processed = False

    # This is the main loop that the program will run.
    # States and their associated value:
    #
    # no_user = 0
    # prog_lt_tqp = 1
    # Process_Song = 2
    # prog_gt_tqp = 3
    # wait_for_resume = 4
    while True:

        # Spotify Authentication
        sp.update_obj()

        # No User
        if state == 0:
            if sp.sp_obj is not None:
                if not sp.ct_is_playing:
                    state = 4
                    printed = False

                else:
                    state = 1
                    printed = False
            else:
                check_printed(printed, state)
                state = 0
                printed = True

        # Progress < 3/4 track Lenght
        elif state == 1 and sp.sp_obj is not None:
            if not sp.ct_is_playing:
                state = 4
                printed = False

            elif (sp.ct_is_playing and
                  (3*sp.ct_length)/4 < sp.ct_progress and
                  not song_processed and
                  sp.ct_uri == prev_tr_uri):
                state = 2
                printed = False

            else:
                # If the song is different from the previous song, then set tweeted to false
                if sp.ct_uri != prev_tr_uri:
                    song_processed = False

                prev_tr_uri = sp.ct_uri
                check_printed(printed, state)
                state = 1
                printed = True

        # Process Song
        elif state == 2:

            # Apparently it is possible to get into this state without a valid obj
            if sp.sp_obj is not None and sp.ct_name == "":
                print("[{}]\033[31mWaring!\u001b[0m: Spotify object exists but no data filled! Forcing state 0!".format(
                    get_curr_time()))
                state = 0
                continue

            process_song(sp, state)
            prev_tr_uri = sp.ct_uri
            state = 3
            printed = False

        # Progress > 3/4 track length && Tweeted
        elif state == 3 and sp.sp_obj is not None:
            if not sp.ct_is_playing:
                state = 4
                printed = False

            elif sp.ct_uri != prev_tr_uri:
                state = 1
                printed = False
                song_processed = False

            else:
                check_printed(printed, state)
                state = 3
                printed = True

        # Waiting for Playback to be Resumed
        elif state == 4 and sp.sp_obj is not None:
            if sp.ct_is_playing:
                if song_processed:
                    state = 3
                    printed = False

                else:
                    state = 1
                    printed = False

            else:
                check_printed(printed, state)
                state = 4
                printed = True

        # Correction for falling out of state, (Not State 0 but also sp_obj is None)
        # Essentially resetting to the default state
        else:
            state = 0
            printed = False

        # Add a sleep(5) as to not spam either Api
        time.sleep(5)


def main():
    # Verifing valid log file
    try:
        testfile = open(sys.argv[1], "r")
    except IOError:
        print("Invalid Log File!\nUsage: ./app.py <logfile>")
        raise

    testfile.close()

    # Enables Proper Logging of the program
    try:
        mainLoop()
    except Exception as e:
        with open(sys.argv[1], "a") as log:
            currTime = get_curr_time()
            tb = sys.exc_info()
            log.write(
                "---------------------------------------------------------------------------\n")
            log.write("[{}] An Error has occured!: {}\n".format(
                str(currTime), repr(e)))
            traceback.print_tb(tb[2], file=log)
            log.write(
                "--------------------------------END LOGFILE--------------------------------\n")
        raise


main()
