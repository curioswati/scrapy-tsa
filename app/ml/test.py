
import numpy
import csv
import re, nltk
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import os

this_path = os.path.dirname(os.path.realpath(__file__))

# import ipdb;ipdb.set_trace()
def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(text):
    # remove non letters
    text = re.sub("[^a-zA-Z]", " ", text)
    # tokenize
    tokens = nltk.word_tokenize(text)
    # stem
    stems = stem_tokens(tokens, stemmer)
    return stems

def test_tweet(tweets):
    if type(tweets) == str:
        tweets = [tweets]

    print "testing..."
    X_new_counts = vectorizer.transform(tweets)
    X_new_tfidf = tfidf_transformer.transform(X_new_counts)

    predicted = model.predict(X_new_tfidf)
    return predicted


stemmer = PorterStemmer()
print(this_path + "/" +  "twitter_MultinomialNB_model.pkl"



    )
# import ipdb;ipdb.set_trace()
model = joblib.load(this_path + "/" +  "twitter_MultinomialNB_model.pkl")
vectorizer = joblib.load(this_path + "/" +  "vectorizer.pkl")
tfidf_transformer = joblib.load(this_path + "/" + "tfidf_transformer.pkl")

tweets = ['God is love', 'OpenGL on the GPU is fast', "it was a very fantastic experience"]
mood = test_tweet(tweets)
