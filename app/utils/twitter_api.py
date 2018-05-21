import csv
import json
import oauth2
import urllib

from datetime import datetime, timedelta

from app.models import Tweet
from app.utils.classifier import NBClassifier
from django.conf import settings


def make_api_request(url, http_method="GET", post_body=None, http_headers=None):
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


def get_tweets(keyword, params={}):
    '''
    Get tweets from twitter based on few params.
    '''
    maxTweets = 50
    url = settings.TWITTER_API_URL
    data = {'q': keyword, 'lang': 'en',
            'count': maxTweets, 'include_entities': 0}

    url += urllib.urlencode(data)

    response = make_api_request(url)
    json_data = json.loads(response)
    tweets = []

    if 'errors' in json_data:
        print "API Error:\n{}".format(json_data['errors'])
    else:
        for item in json_data['statuses']:
            tweets.append((item['id_str'], item['created_at'], item['text']))
    return tweets


def get_bundled_tweets(keyword, from_date, to_date):
    '''
    This function works as an interface between twitter api call and the get_twitter_data
    funtion, it makes call to the function that fetches tweets, arrange the tweets in required
    format and also saves them back to the disc in data directory.

    params:
      keyword - (str) search term
      from_date - (datetime.date object)
      to_date - (datetime.date object)

    returns:
      tweet_bundle - (dict:: {date_str: [tweet1, ]}) tweets arranged according to date of creation.
    '''
    date_format = '%Y-%m-%d'

    # make call to the function to fetch tweets for given date range.
    params = {'since': from_date, 'until': to_date}
    tweets_data = get_tweets(keyword, params)

    # this will be the final output data structure
    tweet_bundle = {}

    for tweet_id, created_at_str, tweet in tweets_data:
        # split and collect the date from created_at string.
        date_parts = created_at_str.split()
        date_str = ' '.join(date_parts[1:3] + date_parts[-1:-2:-1])
        date = datetime.strptime(date_str, '%b %d %Y')
        formatted_date = datetime.strftime(date, date_format)

        # assign the tweet to date in the output DS.
        if formatted_date in tweet_bundle:
            tweet_bundle[formatted_date].append(tweet)
        else:
            tweet_bundle[formatted_date] = [tweet]
        tweet = Tweet.objects.create(tweet_id=tweet_id, text=tweet, created_at=created_at_str, collected_at=date)
        tweet.save()

    return tweet_bundle


def get_twitter_data(keyword, from_date, to_date):
    '''
    This function returns tweets to the view. It first checks if tweets for the required
    date range are available in data directory, if not then it further calls another funtion
    to fetch the tweets and returns the date in required format to the view.
    params:
      keyword - (str) search term
      from_date - (str:: YYYY-mm-dd)
      to_date - (str:: YYYY-mm-dd)

    returns:
      tweets - (dict:: {date_str: [tweet1, ]} ) tweets arranged according to date of creation.
    '''
    date_format = '%Y-%m-%d'
    day_diff = timedelta(days=1)

    from_date = datetime.strptime(from_date, date_format)
    to_date = datetime.strptime(to_date, date_format)

    cur_date = from_date
    tweets_data = {}

    while cur_date <= to_date:
        date_str = datetime.strftime(cur_date, date_format)
        tweets = Tweet.objects.filter(created_at=cur_date).values_list('text', 'sentiment__name')

        if tweets:
            tweets_data[date_str] = tweets
            cur_date += day_diff
        else:
            tweet_bundle = get_bundled_tweets(keyword, cur_date, to_date)
            tweets_data.update(tweet_bundle)
            break
    return tweets_data


def write_to_csv(keyword, tweets):
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


def get_sentiments(tweets_data):
    training_datafile = 'app/data/training.csv'
    nb_classifier_dumpfile = 'app/data/naivebayes_trained_model.pickle'
    nbc = NBClassifier(training_datafile, nb_classifier_dumpfile)
    results = nbc.classify(tweets_data)
    return results
