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


class NaiveBayes:

    def train(self):
        pass

    def apply(self):
        pass
