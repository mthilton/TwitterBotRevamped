class env:

    def __init__(self):
        keys_file = open("keys.txt", "r")

        keys = keys_file.readlines()

        self.twit_consumer_key = keys[0].strip()
        self.twit_consumer_secret = keys[1].strip()
        self.twit_access_token_key = keys[2].strip()
        self.twit_access_token_secret = keys[3].strip()
