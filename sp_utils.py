import spotipy
import spotipy.util as util
import spotipy.oauth2 as auth

class spot(object):

    class SpotEnvError(Exception):
        pass


    def __init__(self, env = None):

        '''
        Creates a Spotify Obj. Will contain all the information that is needed
        to pass into the database/tweet
        '''

        self.sp_oauth = None
        self.token_info = None
        self.token_valid = False
        self.access_token = str()
        self.sp_obj = None
        self.ct_name = str()
        self.ct_uri = str()
        self.ct_num_artists = int()
        self.ct_artists = str()
        self.ct_artists_list = []
        self.ct_artist_uri = {}
        self.ct_url = str()
        self.ct_progress = int()
        self.ct_length = int()
        self.ct_is_playing = False
        self.tweeted = False

        self.update_obj(env)

    def __strip_uri(self, uri):
        new_uri = uri.split(":")
        return new_uri[-1]

    # Authenticates the user, and holds the access token information
    # Essentially a copy paste of the function in spotipy.utils.
    # However I want to be able to refresh the token when it expires
    def get_token_info(self, env):

        if env is None:
            raise SpotEnvError("Enviornment Variables not found!")

        client_id = env.spot_client_id
        client_secret = env.spot_client_secret
        redirect_uri = env.spot_redirect_uri
        cache_path = ".cache-" + env.spot_username
        self.sp_oauth = auth.SpotifyOAuth(client_id,
                                            client_secret,
                                            redirect_uri,
                                            scope='user-read-currently-playing',
                                            cache_path=cache_path)

        # try to get a valid token for this user, from the cache,
        # if not in the cache, the create a new (this will send
        # the user to a web page where they can authorize this app)

        token_info = self.sp_oauth.get_cached_token()

        if not token_info:
            print('''
                User authentication requires interaction with your
                web browser. Once you enter your credentials and
                give authorization, you will be redirected to
                a url.  Paste that url you were directed to to
                complete the authorization.
            ''')
            auth_url = self.sp_oauth.get_authorize_url()
            try:
                import webbrowser
                webbrowser.open(auth_url)
                print("Opened %s in your browser" % auth_url)
            except:
                print("Please navigate here: %s" % auth_url)

            print()
            print()
            try:
                response = raw_input("Enter the URL you were redirected to: ")
            except NameError:
                response = input("Enter the URL you were redirected to: ")

            print()
            print()

            code = self.sp_oauth.parse_response_code(response)
            return self.sp_oauth.get_access_token(code)

        else:
            return token_info

    def update_obj(self, env):

        # Checks to see if we have a token. If we do not, then we aquire one
        if self.token_info is None:
            self.token_info = self.get_token_info(env)
            self.token_valid = self.sp_oauth.is_token_expired(self.token_info)
            self.access_token = self.token_info['access_token']

        # Checks to see if the stored token is valid. If it is not, then refresh it
        if not self.token_valid:
            self.token_info = self.sp_oauth.refresh_access_token(self.token_info['refresh_token'])

            # If the token failed to be refreshed for some reason, get a brand new
            # token
            if self.token_info is None:
                self.token_info = self.get_token_info(env)

            self.token_valid = auth.is_token_expired(self.token_info)
            self.access_token = self.token_info['access_token']

        # Using the valid tokens, create a spotify obj
        self.sp_obj = spotipy.Spotify(auth=self.access_token)

        # Using the spotify obj get the current track
        payload = self.sp_obj.current_user_playing_track()

        if payload is None:
            self.ct_name = str()
            self.ct_uri = str()
            self.ct_num_artists = int()
            self.ct_artists = str()
            self.ct_artists_list = []
            self.ct_artist_uri = {}
            self.ct_url = str()
            self.ct_progress = int()
            self.ct_length = int()
            self.ct_is_playing = False
            self.tweeted = False
            return

        # update the obj values with the new info
        self.ct_name = payload['item']['name']
        self.ct_uri = self.__strip_uri(payload['item']['uri'])
        self.ct_num_artists = len(payload['item']['artists'])
        self.ct_url = payload['item']['external_urls']['spotify']
        self.ct_progress = payload['progress_ms']
        self.ct_length = payload['item']['duration_ms']
        self.ct_is_playing = payload['is_playing']

        # Since there can be multiple artists, create a string where we concat
        # all of the artists onto said string. To store the uri's
        # We will use a dictionary. The keys are the Uri's and the values are
        # the artists names'

        ar = str()
        ar_name = str()
        ar_uri = str()
        self.ct_artists_list = []

        if payload["item"]["artists"][0]["name"] == "Various Artists":

            self.ct_num_artists = self.ct_num_artists - 1

            for i in payload["item"]["artists"][1:]:
                ar_name = i["name"]
                ar_uri = i["uri"]
                ar_uri = self.__strip_uri(ar_uri)
                self.ct_artist_uri[ar_uri] = ar_name
                self.ct_artists_list.append(ar_name)

                ar += ar_name
                if i is not payload["item"]["artists"][-1]:
                    ar += ", "

        else:

            for i in range(self.ct_num_artists):
                ar_name = payload["item"]["artists"][i]["name"]
                ar_uri = payload["item"]["artists"][i]["uri"]
                ar_uri = self.__strip_uri(ar_uri)
                self.ct_artist_uri[ar_uri] = ar_name
                self.ct_artists_list.append(ar_name)

                ar += ar_name
                if i < self.ct_num_artists - 1:
                    ar += ", "

        self.ct_artists = ar
