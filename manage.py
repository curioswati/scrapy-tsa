#!/usr/bin/env python
import os
import sys
import re
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

stemmer = PorterStemmer()
model = joblib.load(this_path + "/app/ml/" + 'twitter_MultinomialNB_model.pkl')
vectorizer = joblib.load(this_path + "/app/ml/"  + 'vectorizer.pkl')
tfidf_transformer = joblib.load(this_path + "/app/ml/"  + 'tfidf_transformer.pkl')

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scrapy-tsa.settings")


    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
