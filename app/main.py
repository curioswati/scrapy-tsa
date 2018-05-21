import pickle
import sys

from app.utils.classifier import SVMClassifier


def train_model(test_tweets_file):
    '''
    This function trains the svm classifier using the training data.
    '''
    training_datafile = 'app/data/training.csv'
    svm_classifier_dumpfile = 'app/data/svm_trained_model.pickle'

    sys.stdout.flush()
    sc = SVMClassifier(training_datafile, svm_classifier_dumpfile, training_required=1)

    # get tweets from file
    tweets_file = open(test_tweets_file)
    tweets = pickle.load(tweets_file)
    tweets_file.close()

    print 'Classifying'
    sys.stdout.flush()
    results = sc.classify(tweets)

    for key in results:
        for item in results[key]:
            print results[key][item]

    print 'Computing Accuracy'
    sc.accuracy()
    print 'Done'
    sys.stdout.flush()
