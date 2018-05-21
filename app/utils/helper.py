import re

from app.utils import common


def get_SVM_feature_vector(feature_list, tweets):
    sorted_features = sorted(feature_list)
    map = {}
    feature_vector = []

    for t in tweets:
        map = {}
        # Initialize empty map
        for w in sorted_features:
            map[w] = 0

        # Fill the map
        for word in t:
            if word in map:
                map[word] = 1

        values = map.values()
        feature_vector.append(values)
    return feature_vector


def get_SVM_feature_vector_and_labels(feature_list, tweets):
    sorted_features = sorted(feature_list)
    map = {}
    feature_vector = []
    labels = []
    for t in tweets:
        label = 0
        map = {}

        # Initialize empty map
        for feature in sorted_features:
            map[feature] = 0

        tweet_words = t[0]
        tweet_opinion = t[1]

        # Fill the map
        for word in tweet_words:
            # process the word (remove repetitions and punctuations)
            word = common.replace_two_or_more(word)
            word = word.strip('\'"?,.')
            # set map[word] to 1 if word exists
            if word in map:
                map[word] = 1

        values = map.values()
        feature_vector.append(values)
        if(tweet_opinion == 'positive'):
            label = 0
        elif(tweet_opinion == 'negative'):
            label = 1
        elif(tweet_opinion == 'neutral'):
            label = 2
        labels.append(label)

    # return the list of feature_vector and labels
    return {'feature_vector': feature_vector, 'labels': labels}


def get_feature_vector(tweet, stop_words):
    '''
    Create feature vector from sample data. This will be words from tweets
    which determines the sentiment of the tweet.
    '''
    feature_vector = []

    # split tweet into words
    words = tweet.split()

    for w in words:
        # replace two or more with two occurrences
        w = common.replace_two_or_more(w)
        # strip punctuation
        w = w.strip('\'"?,.')
        # check if the word stats with an alphabet
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
        # ignore if it is a stop word
        if(w in stop_words or val is None):
            continue
        else:
            feature_vector.append(w.lower())
    return feature_vector
