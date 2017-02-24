#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
---------------------------------
Basics of Naive Bayes Classifiers
---------------------------------

From the definition of conditional probability:
P(outcome ∩ evidence1 ∩ evidence2 ∩ evidence3 ∩ ... ∩ evidenceN)
= P(outcome | evidence1 ∩ evidence2 ∩ evidence3 ∩ ... ∩ evidenceN) × P(evidence1 ∩ evidence2 ∩ evidence3 ∩ ... ∩ evidenceN)
= P(evidence1 ∩ evidence2 ∩ evidence3 ∩ ... ∩ evidenceN | outcome) × P(outcome)
= P(evidence1 | evidence2 ∩ evidence3 ∩ ... ∩ evidenceN ∩ outcome) × ... × P(evidenceN-1 | evidenceN ∩ outcome) × P(evidenceN | outcome) × P(outcome)

Because we assume all evidences are independent:
= P(evidence1 | outcome) × ... × P(evidenceN-1 | outcome) × P(evidenceN | outcome) × P(outcome)

Our goal is to find:
P(outcome | evidence1 ∩ evidence2 ∩ evidence3 ∩ ... ∩ evidenceN)
= P(evidence1 | outcome) × P(evidence2 | outcome) × P(evidence3 | outcome) × ... × P(evidenceN | outcome) × P(outcome) /
  P(evidence1 ∩ evidence2 ∩ evidence3 ∩ ... ∩ evidenceN)

Again, because we assume all evidences are independent:
= P(evidence1 | outcome) × P(evidence2 | outcome) × P(evidence3 | outcome) × ... × P(evidenceN | outcome) × P(outcome) /
  (P(evidence1) × P(evidence2) × P(evidence3) × ... × P(evidenceN))

For each outcome (i.e. class), calculate the probability.
Our condition belongs to the class that has the highest probability.

Remark:
1. We don't have to calculate P(evidence1) × P(evidence2) × P(evidence3) × ... × P(evidenceN) at all.
2. Use logarithms to avoid floating point underflow.
   i.e. Calculate log(P(evidence1 | outcome)) + log(P(evidence2 | outcome)) + ... + log(P(evidenceN | outcome)) + log(P(outcome)) instead.
3. Use Laplace smoothing to deal with P(evidenceK | outcome) = 0 cases.

--------------------------------------------------
Using Naive Bayes Classifier in Sentiment Analysis
--------------------------------------------------

Four variations:
1. Multinomial Naive Bayes
2. Binarized Multinomial Naive Bayes
3. Bernoulli Naive Bayes
4. Gaussian Naive Bayes

We choose Binarized Multinomial Naive Bayes to get the most accurate sentiment classifications.
Remove duplicate words in each document, then use the algorithm of Multinomial Naive Bayes.
(see Figure 13.2 in http://nlp.stanford.edu/IR-book/html/htmledition/naive-bayes-text-classification-1.html)
"""

import math
import pickle
import random

from models import *


class AutoviviDict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value


class NaiveBayes:

    def __init__(self):
        self.classes = {}
        self.vocs = {}
        self.prior = {}
        self.condprob = AutoviviDict()

    def train(self, classes, docs):
        self.classes = classes
        self.vocs = {word for doc in docs for sentence in doc[0].split('\t') for word in sentence.split(' ')}
        num = len(docs)
        for clazz in self.classes:
            tokens_clazz = {}
            docs_clazz = [doc for doc in docs if doc[1] == clazz]
            num_clazz = len(docs_clazz)
            self.prior[clazz] = num_clazz / num
            texts_clazz = [word for doc in docs_clazz for sentence in doc[0].split('\t') for word in sentence.split(' ')]
            for term in self.vocs:
                tokens_clazz[term] = len([token for token in texts_clazz if token == term])
            denominator = sum([(tokens_clazz[term] + 1) for term in self.vocs])
            for term in self.vocs:
                self.condprob[term][clazz] = (tokens_clazz[term] + 1) / denominator

    def apply(self, doc):
        score = {}
        words = {word for sentence in doc.split('\t') for word in sentence.split(' ') if word in self.vocs}
        for clazz in self.classes:
            score[clazz] = math.log(self.prior[clazz])
            for term in words:
                score[clazz] += math.log(self.condprob[term][clazz])
        return max(score, key=score.get)


def init():
    Sentiment.drop_table(fail_silently=True)
    Sentiment.create_table(fail_silently=True)
    post_count = Post.select().count()
    training_post_count = round(post_count * 0.05)
    training_posts = []
    while len(training_posts) < training_post_count:
        random_post = random.randint(1, post_count)
        post = Post.get(Post.id == random_post)
        if post.message:
            training_posts.append(post.id)
    print('Training posts are: ' + ', '.join(map(lambda x: str(x), training_posts)), end='')
    print(' (' + str(training_post_count) + '/' + str(post_count) + ')')


def prepare():
    # input manually after we have manually tagged each training post
    training_posts = [34, 48, 59, 63, 47, 96, 11, 28]
    training_post_tags = ['pos', 'neg', 'pos', 'pos', 'neg', 'neg', 'pos', 'neg']
    assert len(training_posts) == len(training_post_tags)
    assert set(training_post_tags) == {'pos', 'neg'}
    training_post_msgs = []
    training_post_tags_it = iter(training_post_tags)
    for training_post in training_posts:
        post = Post.get(Post.id == training_post)
        training_post_msgs.append(post.message)
        Sentiment.create(pid=post, manual_tag=next(training_post_tags_it))
        print('"' + str(post.id) + '" inserted')
    naive_bayes = NaiveBayes()
    naive_bayes.train({'pos', 'neg'}, list(zip(training_post_msgs, training_post_tags)))
    with open('sentiment.pickle', 'wb') as file:
        pickle.dump(naive_bayes, file, pickle.HIGHEST_PROTOCOL)


def insert():
    with open('sentiment.pickle', 'rb') as file:
        naive_bayes = pickle.load(file)
    for post in Post.select():
        if post.message:
            auto_tag = naive_bayes.apply(post.message)
            query = Sentiment.update(auto_tag=auto_tag).where(Sentiment.pid == post.id)
            if query.execute() == 0:
                Sentiment.create(pid=post, auto_tag=auto_tag)
            print('"' + str(post.id) + '" inserted')

if __name__ == '__main__':
    init()
    # prepare()
    # insert()
