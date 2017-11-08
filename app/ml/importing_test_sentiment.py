import numpy
import csv
import re, nltk
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import test_sentiment

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

if __name__ == "__main__":
	stemmer = PorterStemmer()
	model = joblib.load('twitter_MultinomialNB_model.pkl')
	vectorizer = joblib.load('vectorizer.pkl')
	tfidf_transformer = joblib.load('tfidf_transformer.pkl')

	tweets = ['God is love', 'OpenGL on the GPU is fast', "it was a very fantastic experience"]
	print test_sentiment.test_tweet(tweets, stemmer, model, vectorizer, tfidf_transformer)
