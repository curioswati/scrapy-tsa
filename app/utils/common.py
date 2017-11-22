import csv
import nltk
import re


def get_stop_wordlist(stop_word_list_filename):
    '''
    Read the stopwords file and build a list
    These are the words which does not impact the classfication.
    They don't have any meaning for sentiments as such, for example: is, the, with etc.
    '''
    stop_words = []
    stop_words.append('AT_USER')
    stop_words.append('URL')

    fp = open(stop_word_list_filename, 'r')
    line = fp.readline()
    while line:
        word = line.strip()
        stop_words.append(word)
        line = fp.readline()
    fp.close()
    return stop_words


def is_ascii(word):
    return all(ord(c) < 128 for c in word)


def process_tweet(tweet):
    '''
    This function processes the tweets and removes extra words/characters
    that are not needed like, usernames, URLs etc.
    '''

    # Convert to lower case
    tweet = tweet.lower()
    # Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet)
    # Convert @username to AT_USER
    tweet = re.sub('@[^\s]+', 'AT_USER', tweet)
    # Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    # Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    # trim
    tweet = tweet.strip('\'"')

    # remove first/last " or 'at string end
    tweet = tweet.rstrip('\'"')
    tweet = tweet.lstrip('\'"')
    return tweet


def replace_two_or_more(s):
    '''
    look for 2 or more repetitions of character and replace with the character itself.
    '''
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)


def get_filtered_training_data(training_datafile):
    fp = open(training_datafile, 'rb')

    reader = csv.reader(fp, delimiter=',', quotechar='"', escapechar='\\')
    tweetItems = []
    for row in reader:
        processed_tweet = process_tweet(row[1])
        sentiment = row[0]

        tweet_item = processed_tweet, sentiment
        tweetItems.append(tweet_item)
    return tweetItems


def gen_features(training_datafile):
    '''
    Function to generate feature list from test data.
    It is used only once and the features are saved in a file that can be later used.
    '''
    stop_words = get_stop_wordlist('app/data/stopwords.txt')
    feature_list_file = open('app/data/feature_list.txt', 'w+')
    tweet_items = get_filtered_training_data(training_datafile)

    all_words = []
    for (tweet, sentiment) in tweet_items:
        tweet = process_tweet(tweet)
        words_filtered = [e.lower() for e in tweet.split() if(is_ascii(e))]

        for word in words_filtered:
            word = replace_two_or_more(word)
            word = word.strip('\'"?,.')
            val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*[a-zA-Z]+[a-zA-Z0-9]*$", word)
            if(word in stop_words or val is None or len(word) < 3):
                continue
            else:
                all_words.append(word)
    freq_dist = nltk.FreqDist(all_words)
    word_features = sorted(freq_dist.items(), key=lambda x: x[1], reverse=True)
    for word, freq in word_features:
        feature_list_file.write('{}\n'.format(word))

    feature_list_file.close()
