import numpy
import csv
import re, nltk
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import os
this_path = os.path.dirname(os.path.abspath(__file__))

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


def test_tweet(tweets, stemmer, model, vectorizer, tfidf_transformer):

	if type(tweets) == str:
		tweets = [tweets]

	print "testing..."
	X_new_counts = vectorizer.transform(tweets)
	X_new_tfidf = tfidf_transformer.transform(X_new_counts)

	predicted = model.predict(X_new_tfidf)
	result = predicted.tolist()
	mood = float(sum(result)) / len(result)
	mood = round(mood, 2)
	return mood


def call_senti(tweets):
	stemmer = PorterStemmer()
	model = joblib.load(this_path + "/" + 'twitter_MultinomialNB_model.pkl')
	vectorizer = joblib.load(this_path + "/" + 'vectorizer.pkl')
	tfidf_transformer = joblib.load(this_path + "/" + 'tfidf_transformer.pkl')
	return test_tweet(tweets, stemmer, model, vectorizer, tfidf_transformer)


if __name__ == "__main__":
	stemmer = PorterStemmer()
	model = joblib.load(this_path + "/" + 'twitter_MultinomialNB_model.pkl')
	vectorizer = joblib.load(this_path + "/" + 'vectorizer.pkl')
	tfidf_transformer = joblib.load(this_path + "/" + 'tfidf_transformer.pkl')

	tweets = ['God is love', 'OpenGL on the GPU is fast', "it was a very fantastic experience"]
	print test_tweet(tweets, stemmer, model, vectorizer, tfidf_transformer)
