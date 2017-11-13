import csv

# import svm
from libsvm.svmutil import (LINEAR, svm_load_model, svm_parameter, svm_predict,
                            svm_problem, svm_save_model, svm_train)
# import os
# import pickle
# import re
from utils import common, pre_processor


class SVMClassifier():
    """ SVM Classifier """
    def __init__(self, data, keyword, time, training_datafile,
                 classifier_dumpfile, training_required=0):

        self.feature_list = open('app/data/feature_list.txt').readlines()
        self.len_tweets = len(data)
        self.orig_tweets = self.get_uniq_data(data)
        self.tweets = self.get_processed_tweets(self.orig_tweets)

        self.results = {}
        self.neut_count = [0] * self.len_tweets
        self.pos_count = [0] * self.len_tweets
        self.neg_count = [0] * self.len_tweets
        self.training_datafile = training_datafile

        self.time = time
        self.keyword = keyword
        # self.html = html_helper.HTMLHelper()

        # call training model
        if(training_required):
            self.classifier = self.get_SVM_trained_classifer(training_datafile, classifier_dumpfile)
        else:
            fp = open(classifier_dumpfile, 'r')
            if(fp):
                self.classifier = svm_load_model(classifier_dumpfile)
            else:
                self.classifier = self.get_SVM_trained_classifer(
                    training_datafile, classifier_dumpfile)

    def get_uniq_data(self, data):
        uniq_data = {}
        for i in data:
            d = data[i]
            u = []
            for element in d:
                if element not in u:
                    u.append(element)
            uniq_data[i] = u
        return uniq_data

    def get_processed_tweets(self, data):
        tweets = {}
        for i in data:
            d = data[i]
            tw = []
            for t in d:
                tw.append(pre_processor.process_tweet(t))
            tweets[i] = tw
        return tweets

    def get_SVM_trained_classifer(self, training_datafile, classifier_dumpfile):
        # read all tweets and labels
        tweet_items = self.get_filtered_training_data(training_datafile)

        tweets = []
        for (words, sentiment) in tweet_items:
            words_filtered = [e.lower() for e in words.split() if(common.is_ascii(e))]
            tweets.append((words_filtered, sentiment))

        results = common.get_SVM_feature_vector_and_labels(self.feature_list, tweets)
        self.feature_vectors = results['feature_vector']
        self.labels = results['labels']

        problem = svm_problem(self.labels, self.feature_vectors)
        # '-q' option suppress console output
        param = svm_parameter('-q')
        param.kernel_type = LINEAR
        # param.show()
        classifier = svm_train(problem, param)
        svm_save_model(classifier_dumpfile, classifier)
        return classifier

    def get_filtered_training_data(self, training_datafile):
        fp = open(training_datafile, 'rb')
        min_count = self.get_min_count(training_datafile)
        min_count = 40000
        neg_count, pos_count, neut_count = 0, 0, 0

        reader = csv.reader(fp, delimiter=',', quotechar='"', escapechar='\\')
        tweetItems = []
        count = 1
        for row in reader:
            processed_tweet = pre_processor.process_tweet(row[1])
            sentiment = row[0]

            if(sentiment == 'neutral'):
                if(neut_count == int(min_count)):
                    continue
                neut_count += 1
            elif(sentiment == 'positive'):
                if(pos_count == min_count):
                    continue
                pos_count += 1
            elif(sentiment == 'negative'):
                if(neg_count == int(min_count)):
                    continue
                neg_count += 1

            tweet_item = processed_tweet, sentiment
            tweetItems.append(tweet_item)
            count += 1
        return tweetItems

    def get_min_count(self, training_datafile):
        fp = open(training_datafile, 'rb')
        reader = csv.reader(fp, delimiter=',', quotechar='"', escapechar='\\')
        neg_count, pos_count, neut_count = 0, 0, 0
        for row in reader:
            sentiment = row[0]
            if(sentiment == 'neutral'):
                neut_count += 1
            elif(sentiment == 'positive'):
                pos_count += 1
            elif(sentiment == 'negative'):
                neg_count += 1
        return min(neg_count, pos_count, neut_count)

    def classify(self):
        for i in self.tweets:
            tw = self.tweets[i]
            test_tweets = []
            res = {}
            for words in tw:
                words_filtered = [e.lower() for e in words.split() if(common.is_ascii(e))]
                test_tweets.append(words_filtered)
            test_feature_vector = common.get_SVM_feature_vector(test_tweets)
            p_labels, p_accs, p_vals = svm_predict([0] * len(test_feature_vector),
                                                   test_feature_vector, self.classifier)
            count = 0
            for t in tw:
                label = p_labels[count]
                if(label == 0):
                    label = 'positive'
                    self.pos_count[i] += 1
                elif(label == 1):
                    label = 'negative'
                    self.neg_count[i] += 1
                elif(label == 2):
                    label = 'neutral'
                    self.neut_count[i] += 1
                result = {'text': t, 'tweet': self.orig_tweets[i][count], 'label': label}
                res[count] = result
                count += 1
            self.results[i] = res

    def write_output(self, filename, write_option='w'):
        fp = open(filename, write_option)
        for i in self.results:
            res = self.results[i]
            for j in res:
                item = res[j]
                text = item['text'].strip()
                label = item['label']
                write_str = text+" | "+label+"\n"
                fp.write(write_str)

    def accuracy(self):
        tweets = self.get_filtered_training_data(self.training_datafile)
        test_tweets = []
        for (t, l) in tweets:
            words_filtered = [e.lower() for e in t.split() if(common.is_ascii(e))]
            test_tweets.append(words_filtered)

        test_feature_vector = common.get_SVM_feature_vector(self.feature_list, test_tweets)
        p_labels, p_accs, p_vals = svm_predict([0] * len(test_feature_vector),
                                               test_feature_vector, self.classifier)
        count = 0
        total, correct, wrong = 0, 0, 0
        self.accuracy = 0.0
        for (t, l) in tweets:
            label = p_labels[count]
            if(label == 0):
                label = 'positive'
            elif(label == 1):
                label = 'negative'
            elif(label == 2):
                label = 'neutral'

            if(label == l):
                correct += 1
            else:
                wrong += 1
            total += 1
            count += 1
        self.accuracy = (float(correct)/total)*100
        print 'Total = {}, Correct = {}, Wrong = {}, Accuracy = {}'.format(
            total, correct, wrong, self.accuracy)

    def get_HTML(self):
        return self.html.get_result_HTML(self.keyword, self.results, self.time, self.pos_count,
                                         self.neg_count, self.neut_count, 'svm')
