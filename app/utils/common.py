import pickle
import re
import sys

from utils import classifier, pre_processor


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
        w = pre_processor.replace_two_or_more(w)
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
# end


def extract_features(feature_list, tweet):
    tweet_words = set(tweet)
    features = {}
    for word in feature_list:
        features['contains(%s)' % word] = (word in tweet_words)
    return features


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
            word = pre_processor.replace_two_or_more(word)
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


def is_ascii(word):
    return all(ord(c) < 128 for c in word)


def train_model(test_tweets_file):
    '''
    This function trains the svm classifier using the training data.
    '''
    # get tweets from file
    tweets_file = open(test_tweets_file)
    tweets = pickle.load(tweets_file)
    tweets_file.close()

    training_datafile = 'app/data/full_training_dataset.csv'
    classifier_dumpfile = 'app/data/svm_trained_model.pickle'
    training_required = 1
    keyword = 'scrapy'
    time = 'lastweek'

    sys.stdout.flush()
    sc = classifier.SVMClassifier(tweets, keyword, time, training_datafile,
                                  classifier_dumpfile, training_required)
    print 'Computing Accuracy'
    sys.stdout.flush()
    sc.classify()
    sc.accuracy()
    print 'Done'
    sys.stdout.flush()
