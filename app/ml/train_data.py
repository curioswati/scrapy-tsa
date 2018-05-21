# -*- coding: utf-8 -*-

import numpy
import csv
import re, nltk
from sklearn.feature_extraction.text import CountVectorizer        
from nltk.stem.porter import PorterStemmer
from sklearn.linear_model import LogisticRegression
# from sklearn.cross_validation import train_test_split
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB


def decode_emoticons(text):
	text = "Sunny Again Work Tomorrow  :-|  TV Tonight"

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

	train_data = {
		"text": [],
		"sentiment": []
	}

	raw_count = 0
	with open('Sentiment Analysis Dataset.csv', 'r') as csvfile:
			csvreader = csv.reader(csvfile)
			headers = next(csvreader, None)
			for line in csvreader:
				train_data["text"].append(line[3].strip())
				train_data["sentiment"].append(int(line[1]))
				# raw_count += 1
				# if raw_count >= 1000:
				# 	break


	raw_count = 0
	with open('training.1600000.processed.noemoticon.csv', 'r') as csvfile:
			csvreader = csv.reader(csvfile)
			for line in csvreader:
				try:
					train_data["text"].append(line[5].strip())
				except Exception as e:
					print e
					print "line", line
					print line[5]
					exit(0)
				if int(line[0]) == 4:
					train_data["sentiment"].append(1)
				else:
					train_data["sentiment"].append(0)
				# raw_count += 1
				# if raw_count >= 1000:
				# 	break

	print train_data["text"][:3]
	print train_data["sentiment"][:3]
	print numpy.unique(numpy.array(train_data["sentiment"]))
	print "data extracted"
	# exit(0)

	stemmer = PorterStemmer()


	vectorizer = CountVectorizer(
	    analyzer = 'word',
	    tokenizer = tokenize,
	    lowercase = True,
	    stop_words = 'english',
	    max_features = 100,
	    encoding='utf-8'
	)

	print "creating corpus_data_features"
	X_train_counts = vectorizer.fit_transform(train_data["text"])
	# tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
	# X_train_tf = tf_transformer.transform(X_train_counts)

	tfidf_transformer = TfidfTransformer()
	X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
	print "X_train_tfidf.shape", X_train_tfidf.shape

	print "training"
	model = MultinomialNB().fit(X_train_tfidf, train_data["sentiment"])
	joblib.dump(model, 'twitter_MultinomialNB_model.pkl', compress=1)
	joblib.dump(vectorizer, 'vectorizer.pkl', compress=1)
	joblib.dump(tfidf_transformer, 'tfidf_transformer.pkl', compress=1)


	docs_new = ['God is love', 'OpenGL on the GPU is fast', "it was a very fantastic experience"]
	X_new_counts = vectorizer.transform(docs_new)
	X_new_tfidf = tfidf_transformer.transform(X_new_counts)

	predicted = model.predict(X_new_tfidf)
	print "predicted", predicted

	print model.score(X_train_tfidf, train_data["sentiment"])
