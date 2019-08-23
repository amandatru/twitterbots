import tweepy
import os
from musixmatch.api import Musixmatch
import swagger_client
from swagger_client.rest import ApiException

#env vars to not store keys in code
musixmatch_api_key = os.getenv("API_KEY")
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_secret = os.getenv("ACCESS_TOKEN_SECRET")

# initializing api clients
def create_twitter_api():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    return api

def create_swagger_client():
    swagger_client.configuration.api_key['apikey'] = musixmatch_api_key;
    return swagger_client

def create_musixmatch_api():
    musixmatch = Musixmatch(musixmatch_api_key)
    return musixmatch
