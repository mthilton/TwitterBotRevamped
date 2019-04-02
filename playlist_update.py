#!/usr/bin/env python3

import sys, time, twitter, spotipy
import datetime, traceback
import mysql.connector
import spotipy.util as util

sys.path.append('../')
from env import env

e = env()
alltime_playlist_uri = e.alltime_pl
weekly_playlist_uri = e.weekly_pl

twit = twitter.Api(consumer_key=e.twit_consumer_key,
                    consumer_secret=e.twit_consumer_secret,
                    access_token_key=e.twit_access_token_key,
                    access_token_secret=e.twit_access_token_secret)

mydb = mysql.connector.connect(host=e.mysql_host,
                                user=e.mysql_user,
                                passwd=e.mysql_pw,
                                database=e.mysql_db)

scope = 'playlist-modify-public playlist-modify-private'
token = util.prompt_for_user_token(username=e.spot_username,
                                    scope=scope,
                                    client_id=e.spot_client_id,
                                    client_secret= e.spot_client_secret,
                                    redirect_uri=e.spot_redirect_uri)

# On success grab the current user playing track
if token:
    sp = spotipy.Spotify(auth=token)

# Otherwise authentication failed and we will kill the program
else:
    print ("Can't get token for " + e.spot_username)
    exit()

mycursor = mydb.cursor()
query1 = """SELECT tr_uri \
           FROM SpTrackInfo \
           ORDER BY AllTime_Num_Playbacks DESC, tr_name ASC \
           LIMIT 50"""

query2 = """SELECT tr_uri \
           FROM SpTrackInfo \
           ORDER BY Weekly_Num_Playbacks DESC, tr_name ASC \
           LIMIT 50"""

mycursor.execute(query1)
alltime_payload = mycursor.fetchall()

mycursor.execute(query2)
weekly_payload = mycursor.fetchall()

alltime = []
weekly = []

for x in range(0,49):
    alltime.append(alltime_payload[x][0])
    weekly.append(weekly_payload[x][0])

sp.user_playlist_replace_tracks(e.spot_username, alltime_playlist_uri, alltime)
sp.user_playlist_replace_tracks(e.spot_username, weekly_playlist_uri, weekly)

print("Sucessfully updated both playlists!")

query3 = """UPDATE SpTrackInfo \
            SET Weekly_Num_Playbacks = 0"""

try:
    mycursor.execute(query3)
    mydb.commit()
    print(mycursor.rowcount, "records updated in table SpTrackInfo in DB TBR.")

except mysql.connector.Error as error:
    mydb.rollback() # rollback if any exception occured
    print("Failed updating records into SpTrackInfo {}".format(error))

finally:

    # closing database connection.
    if(mydb.is_connected()):
        mycursor.close()
        mydb.close()
