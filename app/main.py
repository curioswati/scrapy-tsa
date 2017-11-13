import pickle
import sys

from utils import classifier, common

# Read the tweets one by one and process it
# inp_tweets = csv.reader(open('app/data/sampleTweets.csv', 'rb'), delimiter=',', quotechar='|')
# fp = open('app/data/sampleTweets.txt', 'r')
# line = fp.readline()

stop_words = common.get_stop_wordlist('app/data/stopwords.txt')

# tweets = []
feature_list = []
#
# for row in inp_tweets:
#     sentiment = row[0]
#     tweet = row[1]
#     processed_tweet = pre_processor.process_tweet(tweet)
#     feature_vector = common.get_feature_vector(processed_tweet, stop_words)
#     feature_list.extend(feature_vector)
#     tweets.append((feature_vector, sentiment))
#
feature_list = list(set(feature_list))


def extract_features(tweet):
    tweet_words = set(tweet)
    features = {}
    for word in feature_list:
        features['contains(%s)' % word] = (word in tweet_words)
    return features


# get tweets from file
tweets_file = open('app/data/weekTweets_iphone_1596.txt')
tweets = pickle.load(tweets_file)
tweets_file.close()

training_datafile = 'app/data/full_training_dataset.csv'
classifier_dumpfile = 'app/data/svm_trained_model.pickle'
training_required = 1
keyword = 'scrapy'
time = 'daily'

sys.stdout.flush()
sc = classifier.SVMClassifier(tweets, keyword, time, training_datafile,
                              classifier_dumpfile, training_required)
print 'Computing Accuracy'
sys.stdout.flush()
sc.accuracy()
print 'Done'
sys.stdout.flush()
