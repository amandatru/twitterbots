import tweepy
from datetime import datetime, time, timedelta
from musixmatch_script import generate_fortune
from config_script import create_twitter_api
import time


#retrieve most recent tweet in case bot has to restart
def get_starting_fortune():
    recent_tweets = api.mentions_timeline(count=1)
    since_id = recent_tweets[0].id_str
    return since_id

#function to generate and tweet fortune
def post_fortune(tweetid, handle):
    fortune_array = generate_fortune()
    status = "@" + handle + " \nYour EDM Fortune Cookie says... \n" +"\"" + fortune_array[1] + "\"\n" + "Song: " + fortune_array[2] + "\nArtist: " + fortune_array[0]
    print(status)
    api.update_status(status, in_reply_to_status_id=tweetid)
    print('posted fortune: success')

#scan for new mentions with keyword 'fortune'
def scan_mentions(since_id):
    while True:
        print('in while loop')
        print('since_id')
        print(since_id)
        mentions = api.mentions_timeline(since_id=since_id)
        now = datetime.utcnow()
        for mention in mentions:
            print('STATUS')
            print(mention.user.screen_name)
            print(mention.id)
            print(mention.text)
            print('since_id')
            print(since_id)
            print('mention_id')
            print(mention.id)
            # set cursor to latest tweet
            since_id = max(int(mention.id), int(since_id))
            print('max')
            print(since_id)
            #searching for keyword fortune
            if "fortune" in mention.text.lower():
                print('posting fortune')
                # raise Exception('fake exception!')
                post_fortune(mention.id, mention.user.screen_name)
            else:
                print('no match')
        # call mentions_timeline every 12 seconds bc of api restriction
        time.sleep(12)

def print_mentions():
    mentions = api.mentions_timeline()
    for mention in mentions:
        print(mention.id, mention.author.screen_name, mention.text)

api = create_twitter_api()
# getting most recent tweet in case bot resets
since_id = get_starting_fortune()
# infinite loop to keep scanning mentions
while True:
    try:
        print('scan mentions()')
        scan_mentions(since_id)
    except:
        print('exception thrown')
        time.sleep(2)
        continue
