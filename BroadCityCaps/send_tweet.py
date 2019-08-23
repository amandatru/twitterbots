import requests
import tweepy
import boto3
import botocore
import os
import random

# env vars to not store keys in code
consumer_key = os.environ['consumer_key']
consumer_secret = os.environ['consumer_secret']
access_token = os.environ['access_token']
access_secret = os.environ['access_secret']

#Event, context parameters required for AWS Lambda
def send_tweet(event, context):
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	#Twitter requires all requests to use OAuth for authentication
	auth.set_access_token(access_token, access_secret)
	api = tweepy.API(auth)
	s3 = boto3.resource('s3')
	BUCKET_NAME = 'broadcity'

	keyArray = []

	s3bucket = s3.Bucket(BUCKET_NAME)
	randomSeason = random.randint(1,4)
	randomEpisode = random.randint(1,10)
	# convert int values to string for looking up key in S3
	randomSeason = str(randomSeason)
	randomEpisode = str(randomEpisode)

	#filter out all objects based on season # and episode #
	for obj in s3bucket.objects.filter(Prefix=randomSeason+"/"+randomEpisode):
			#add all frame key values from episode to an array
			keyArray.append('{0}'.format(obj.key))

	#get number of frames for an episode based on length of array
	numFrames = (len(keyArray))

	# get a random frame number
	randomFrame = random.randint(0,numFrames)

	#grab frame key from array
	KEY = (keyArray[randomFrame])

	#download frame jpg from s3 and save to /tmp
	pic = s3.Bucket(BUCKET_NAME).download_file(KEY, '/tmp/local.png')
	user=api

	#tweet pic with hashtag
	status = '#BroadCity'
	user.update_with_media('/tmp/local.png', status)

	#delete tmp img
	os.remove('/tmp/local.png')

	return KEY
