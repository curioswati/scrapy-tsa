#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv
import json
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()


#Twitter API credentials
consumer_key = os.environ.get('TWITTER_CONSUMER_KEY')
consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET')
access_key = os.environ.get('TWITTER_ACCESS_TOKEN')
access_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')


def wrtite_to_csv(screen_name, alltweets):
    # transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
    # write the csv
    with open('%s_tweets.csv' % screen_name, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "created_at", "text"])
        writer.writerows(outtweets)


def write_to_json(screen_name, alltweets):
    outtweets = [{tweet.id_str: {'created_at': str(tweet.created_at), 'place': str(tweet.place),
                  'geo': str(tweet.geo), 'text': tweet.text.encode("utf-8")}} for tweet in alltweets]
    # write the json
    with open('%s_tweets.json' % screen_name, 'wb') as f:
        json.dump(outtweets, f)


def get_all_tweets(screen_name):
    #Twitter only allows access to a users most recent 3240 tweets with this method
    # assuming rate limit hit
    status = 0

    try:
        tweets = []
        #authorize twitter, initialize tweepy
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        api = tweepy.API(auth)

        #initialize a list to hold all the tweepy Tweets
        alltweets = []

        #make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = api.user_timeline(screen_name = screen_name,count=200)

        #save most recent tweets
        alltweets.extend(new_tweets)
        status = 1

        #save the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        #keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0:
            print "getting tweets before %s" % (oldest)

            #all subsiquent requests use the max_id param to prevent duplicates
            new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)

            #save most recent tweets
            alltweets.extend(new_tweets)

            #update the id of the oldest tweet less one
            oldest = alltweets[-1].id - 1

            print "...%s tweets downloaded so far" % (len(alltweets))
        # write_to_json(screen_name, alltweets)
        tweets = [tweet.text.encode("utf-8") for tweet in alltweets]
        return status, tweets
    except tweepy.error.RateLimitError:
        if status == 1 :
            # in case if few tweets are fetched and rate limit hit
            status = 2
            tweets = [tweet.text.encode("utf-8") for tweet in alltweets]
        return status , tweets



if __name__ == '__main__':
    #pass in the username of the account you want to download
    get_all_tweets("flaper87")
