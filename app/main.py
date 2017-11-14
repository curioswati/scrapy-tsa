from utils import common

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
