#!/usr/bin/env python3

import sys
import spotipy
import spotipy.util as util
import twitter

sys.path.append('../')
from env import env as enviorn

e = enviorn()

print("consumer_key is: " + e.twit_consumer_key)
print("consumer_secret is: " + e.twit_consumer_secret)
print("access_token_key is: " + e.twit_access_token_key)
print("access_token_secret is: " + e.twit_access_token_secret)
print("The last char in consumer_key string is: " + e.twit_consumer_key[-1])

twit = twitter.Api(consumer_key=e.twit_consumer_key,
                  consumer_secret=e.twit_consumer_secret,
                  access_token_key=e.twit_access_token_key,
                  access_token_secret=e.twit_access_token_secret)

status = twit.PostUpdate('I love python-twitter!')

print(status.text)
