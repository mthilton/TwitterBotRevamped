import spotipy
import os
from time import sleep
from spotipy.oauth2 import SpotifyOAuth


class spot(object):

    class SpotEnvError(Exception):
        pass

    class SpotAuthenticationError(Exception):
        pass

    def __init__(self, cache_path=None):
        '''
        Creates a Spotify Obj. Will contain all the information that is needed
        to pass into the database/tweet. For use only with this current_track() only
        '''

        self.__cache_path = cache_path
        self.sp_oauth = None
        self.sp_obj = None
        self.ct_name = str()
        self.ct_uri = str()
        self.ct_num_artists = int()
        self.ct_artists = str()
        self.ct_artist_uri = str()
        self.ct_ar_uri_dict = {}
        self.ct_progress = int()
        self.ct_length = int()
        self.ct_is_playing = False
        self.ct_popularity = int()

        self.__authenticate_user()

        # Using the valid credentials, create a spotify obj
        self.sp_obj = spotipy.Spotify(auth_manager=self.sp_oauth)
        self.update_obj()

    def __sp_obj_none(self):
        self.ct_name = str()
        self.ct_uri = str()
        self.ct_num_artists = int()
        self.ct_artists = str()
        self.ct_artist_uri = str()
        self.ct_ar_uri_dict = {}
        self.ct_progress = int()
        self.ct_length = int()
        self.ct_is_playing = False
        self.ct_popularity = int()
        return

    # Authenticates the user using OAuth 2.0
    # Has support for user defined scope and cache_path
    def __authenticate_user(self):

        if self.__cache_path is None:
            self.__cache_path = "./.cache/sp/app/.cache-" + \
                os.getenv('SPOTIFY_USERNAME')

        self.sp_oauth = SpotifyOAuth(client_id=os.getenv('SPOTIFY_CLIENT_ID'),
                                     client_secret=os.getenv(
                                         'SPOTIFY_CLIENT_SECRET'),
                                     redirect_uri=os.getenv(
                                         'SPOTIFY_REDIRECT_URL'),
                                     scope='user-read-currently-playing',
                                     cache_path=self.__cache_path,
                                     open_browser=False)

        # try to get a valid token for this user, from the cache,
        # if not in the cache, the create a new (this will send
        # the user to a web page where they can authorize this app)

        if self.sp_oauth is None or self.sp_oauth.cache_path is not self.__cache_path:
            raise self.SpotAuthenticationError("Unable to get Authenticated!")

    def update_obj(self):
        payload = None

        # Attempt to update the object
        while payload is None:
            try:
                # Using the spotify obj get the current track
                payload = self.sp_obj.currently_playing()
            except Exception:
                sleep(1)

        # Check to make sure payload is populated
        if payload is None or payload['item'] is None:
            self.__sp_obj_none()
            return

        # update the obj values with the new info
        self.ct_name = payload['item']['name']
        self.ct_uri = payload['item']['id']
        self.ct_num_artists = len(payload['item']['artists'])
        self.ct_progress = payload['progress_ms']
        self.ct_length = payload['item']['duration_ms']
        self.ct_is_playing = payload['is_playing']
        self.ct_popularity = payload['item']['popularity']

        # Since there can be multiple artists, create a string where we concat
        # all of the artists onto said string. To store the uri's
        # We will use a dictionary. The keys are the Uri's and the values are
        # the artists names'

        ar_list = str()
        ar_uri_list = str()
        self.ct_ar_uri_dict = {}

        for ar in payload['item']['artists']:
            ar_uri = ar["id"]

            # Get Artist Name baed on ID
            ar_info = self.sp_obj.artist(artist_id=ar_uri)
            ar_name = ar_info["name"]

            # Add the names to the approtiate data stuctrues and
            # strings
            self.ct_ar_uri_dict[ar_uri] = ar_name
            ar_list += ar_name
            ar_uri_list += ar_uri

            # In the strings, as long as the artist is not the last artist,
            # appaend a comma and a space
            if ar is not payload["item"]["artists"][-1]:
                ar_list += ", "
                ar_uri_list += ", "

        self.ct_artists = ar_list
        self.ct_artist_uri = ar_uri_list
