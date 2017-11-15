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


def extract_features(feature_list, tweet):
    tweet_words = set(tweet)
    features = {}
    for word in feature_list:
        features['contains(%s)' % word] = (word in tweet_words)
    return features


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
