class env:

    def __init__(self):
        keys_file = open("keys.txt", "r")

        keys = keys_file.readlines()

        self.twit_consumer_key = keys[0].strip()
        self.twit_consumer_secret = keys[1].strip()
        self.twit_access_token_key = keys[2].strip()
        self.twit_access_token_secret = keys[3].strip()
        self.spot_username = keys[4].strip()
        self.spot_client_id = keys[5].strip()
        self.spot_client_secret = keys[6].strip()
        self.spot_redirect_uri = keys[7].strip()
        self.mysql_host = keys[8].strip()
        self.mysql_user = keys[9].strip()
        self.mysql_pw = keys[10].strip()
        self.mysql_db = keys[11].strip()
        self.alltime_pl = keys[12].strip()
        self.weekly_pl = keys[13].strip()
        keys_file.close()
