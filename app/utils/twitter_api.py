import csv
import json
import oauth2
import urllib

from datetime import datetime
from django.conf import settings


def make_api_request(self, url, http_method="GET", post_body=None, http_headers=None):
    '''
    Make API request to get tweets.
    '''
    consumer = oauth2.Consumer(key=settings.CONSUMER_KEY, secret=settings.CONSUMER_SECRET)
    token = oauth2.Token(key=settings.ACCESS_TOKEN, secret=settings.ACCESS_TOKEN_SECRET)
    client = oauth2.Client(consumer, token)

    resp, content = client.request(
        url,
        method=http_method,
        body=post_body or '',
        headers=http_headers
    )
    return content


def get_tweets(keyword, params=None):
    '''
    Get tweets from twitter based on few params.
    '''
    maxTweets = 50
    url = settings.TWITTER_API_URL
    data = {'q': keyword, 'lang': 'en', 'result_type': 'recent',
            'count': maxTweets, 'include_entities': 0}

    # Add if additional params are passed
    if params:
        for key, value in params.iteritems():
            data[key] = value

    url += urllib.urlencode(data)

    response = make_api_request(url)
    json_data = json.loads(response)
    tweets = []

    if 'errors' in json_data:
        print "API Error"
        print json_data['errors']
    else:
        for item in json_data['statuses']:
            tweets.append(item['text'])
    return tweets


def wrtite_to_csv(keyword, tweets):
    '''
    Save tweets in a csv file to load later.
    '''
    # transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in tweets]

    # write the csv
    file_name = '/app/data/{}_{}.csv'.format(
        keyword, datetime.strftime(datetime.now(), '%d_%m_%Y_%H:%M:%S'))

    with open(file_name, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "created_at", "text"])
        writer.writerows(outtweets)


def write_to_json(keyword, tweets):
    '''
    Save tweets in a json file to load later.
    '''
    outtweets = [{tweet.id_str: {'created_at': str(tweet.created_at), 'place': str(tweet.place),
                  'geo': str(tweet.geo), 'text': tweet.text.encode("utf-8")}} for tweet in tweets]

    file_name = '/app/data/{}_{}.json'.format(
        keyword, datetime.strftime(datetime.now(), '%d_%m_%Y_%H:%M:%S'))

    # write the json
    with open(file_name, 'wb') as f:
        json.dump(outtweets, f)
