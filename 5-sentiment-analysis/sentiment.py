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
(see also http://web.stanford.edu/~jurafsky/NLPCourseraSlides.html)
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
            texts_clazz = []
            for doc in docs_clazz:
                words = {word for sentence in doc[0].split('\t') for word in sentence.split(' ')}
                texts_clazz.extend(words)
            for term in self.vocs:
                tokens_clazz[term] = texts_clazz.count(term)
            denominator = sum((tokens_clazz[term] + 1) for term in self.vocs)
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


def prepare(training_posts, training_post_tags):
    assert len(training_posts) == len(training_post_tags)
    assert set(training_post_tags) == {'pos', 'neg'}
    # assert training_post_tags.count('pos') == training_post_tags.count('neg')
    training_post_msgs = []
    training_post_tags_it = iter(training_post_tags)
    for training_post in training_posts:
        post = Post.get(Post.id == training_post)
        training_post_msgs.append(post.message)
        manual_tag = next(training_post_tags_it)
        query = Sentiment.update(manual_tag=manual_tag).where(Sentiment.pid == post.id)
        if query.execute() == 0:
            Sentiment.create(pid=post, manual_tag=manual_tag)
    naive_bayes = NaiveBayes()
    naive_bayes.train({'pos', 'neg'}, list(zip(training_post_msgs, training_post_tags)))
    with open('sentiment.pickle', 'wb') as file:
        pickle.dump(naive_bayes, file, pickle.HIGHEST_PROTOCOL)


def validate(testing_posts, testing_post_tags):
    with open('sentiment.pickle', 'rb') as file:
        naive_bayes = pickle.load(file)
    assert len(testing_posts) == len(testing_post_tags)
    assert set(testing_post_tags) == {'pos', 'neg'}
    # assert testing_post_tags.count('pos') == testing_post_tags.count('neg')
    hit_count = 0
    testing_post_tags_it = iter(testing_post_tags)
    for testing_post in testing_posts:
        post = Post.get(Post.id == testing_post)
        auto_tag = naive_bayes.apply(post.message)
        if next(testing_post_tags_it) == auto_tag:
            hit_count += 1
            print('P', end='')
        else:
            print('F', end='')
    print()
    return hit_count / len(testing_posts) * 100


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


def ten_fold_cross_validation():
    posts = [
        15559, 8059, 853, 16964, 17319, 17709, 13538, 5585, 17024, 13365,
        927, 12586, 9926, 2717, 7324, 18104, 9116, 4017, 1806, 7466, 13162,
        3224, 14682, 9875, 17321, 3707, 13968, 2622, 10917, 11826, 9685,
        4197, 17477, 7435, 3966, 6134, 9742, 7739, 14439, 442, 5568, 16263,
        2635, 12294, 15179, 3424, 16704, 7335, 16975, 13667, 8135, 8542,
        15304, 10553, 11718, 3194, 2048, 5516, 18619, 7130, 2082, 17896,
        16309, 8233, 2688, 8789, 18452, 11147, 16726, 1535, 15443, 631,
        1107, 16940, 12272, 17885, 12875, 5157, 2517, 5633, 11268, 15029,
        12598, 16182, 11369, 17354, 18777, 2065, 8355, 14424, 92, 783,
        14020, 16035, 14710, 2772, 17083, 2397, 15073, 9640, 10456, 3769,
        13152, 3784, 7846, 9169, 4032, 4857, 15813, 15018, 6291, 5499,
        9107, 5270, 6264, 12146, 765, 15475, 8717, 18615, 7871, 15662,
        3632, 14259, 3327, 13918, 16832, 565, 14019, 4389, 11146, 6113,
        16575, 8618, 18049, 18956, 16020, 4521, 12233, 18430, 17145, 18617,
        6879, 9041, 8350, 16520, 981, 2775, 15499, 17732, 2525, 15724, 463,
        3096, 8993, 1265, 4571, 6178, 18390, 3015, 9780, 1158, 5291, 5935,
        4923, 4710, 15795, 15632, 11916, 16485, 3720, 17122, 13883, 2589,
        15476, 1582, 3302, 2661, 5145, 11952, 10933, 8381, 6077, 3029, 531,
        14659, 3283, 2362, 8597, 6608, 1747, 10977, 15826, 10163, 2909,
        17461, 15913, 8577, 9877, 7799, 10562, 16880, 5629, 12575, 18221,
        15254, 15142, 16333, 12844, 4355, 7793, 17510, 15405, 1374, 7712,
        4060, 5788, 14370, 4708, 4802, 16486, 13078, 15149, 12024, 6930,
        8771, 17530, 498, 3845, 18685, 10675, 15719, 1197, 9841, 12284,
        13382, 2927, 12398, 2976, 13410, 9025, 18939, 4075, 16089, 4281,
        15579, 12037, 12174, 7459, 16365, 4419, 15799, 2754, 7342, 8534,
        9750, 5298, 4613, 7389, 12591, 17193, 3079, 12079, 10189, 8058, 11,
        8345, 16718, 16687, 12685, 9404, 17472, 566, 2692, 87, 12356,
        12868, 1941, 355, 2582, 4161, 15297, 2770, 2071, 1193, 11645,
        15052, 2988, 15806, 420, 6761, 18387, 2758, 13166, 9908, 11857,
        16073, 16227, 5999, 5257, 7449, 13607, 17522, 10521, 6781, 12350,
        599, 18801, 10626, 11138, 13114, 13204, 10389, 14146, 1352, 12888,
        1072, 9825, 3128, 18701, 13018, 6990, 1563, 2349, 3296, 3629, 8066,
        15302, 18388, 1293, 16105, 4311, 3906, 845, 9614, 1611, 17323,
        13597, 10387, 10953, 14047, 1000, 15325, 18312, 9125, 1969, 14107,
        17649, 11995, 1855, 18223, 10718, 1683, 9559, 10311, 6440, 18160,
        13990, 9910, 6239, 14411, 8514, 5073, 11465, 16159, 3552, 14138,
        8536, 14352, 16581, 7790, 16431, 15927, 15003, 3435, 13009, 13799,
        1783, 18871, 5206, 15053, 6855, 6148, 16178, 4882, 9842, 15105,
        7834, 5577, 8040, 5754, 3704, 3388, 18647, 17295, 4139, 18953,
        2940, 7911, 8710, 11968, 9758, 10647, 137, 6005, 7402, 6972, 18118,
        3874, 13323, 2087, 13612, 10905, 9493, 5511, 10604, 10478, 2131,
        177, 1935, 10290, 16310, 9111, 3440, 17955, 1545, 1833, 6631, 4883,
        6691, 2115, 8370, 9214, 16234, 16256, 9416, 4332, 246, 5412, 10164,
        15442, 4179, 13828, 18040, 12029, 9468, 12588, 10792, 12745, 17172,
        14976, 8871, 13746, 8708, 8252, 16514, 11104, 5174, 5603, 12476,
        13080, 7720, 419, 124, 14692, 13839, 4072, 13032, 406, 11063, 7830,
        4951, 10506, 2390, 9274, 15144, 2369, 15782, 15931, 741, 17538,
        3724, 12025, 10698, 13783, 326, 6056, 12620, 4199, 6109, 18906,
        1192, 14954, 5276, 2795, 6438, 5755, 15270, 7399, 15797, 18902,
        11093, 1584, 11658, 8074, 1762, 1137, 12074, 10651, 18686, 17734,
        16250, 11687, 15277, 13581, 6516, 7763, 6094, 7168, 12190, 2100,
        1604, 4814, 15438, 7999, 9380, 17439, 4390, 12650, 3550, 9547,
        15269, 4334, 8851, 7681, 7591, 3353, 464, 2223, 14900, 9990, 8112,
        4318, 15082, 2218, 12237, 8438, 16180, 6600, 8521, 541, 6843,
        14296, 17087, 13526, 18781, 1295, 5719, 2161, 17173, 4066, 8836,
        7140, 9002, 2682, 7070, 5454, 15790, 405, 2776, 14426, 14966,
        14260, 15327, 1717, 17176, 8535, 2088, 2239, 11564, 5226, 11172,
        6388, 5364, 3735, 15439, 14475, 5809, 12483, 4103, 11148, 3086,
        11641, 2509, 9187, 15929, 5150, 18264, 7497, 8026, 426, 12406,
        14408, 4763, 17444, 7794, 11650, 5082, 15061, 10583, 1371, 17223,
        11426, 9535, 12437, 6846, 15989, 990, 3911, 267, 5651, 9011, 3173,
        18627, 6375, 18901, 16528, 8914, 13735, 12688, 7769, 7267, 1834,
        428, 17886, 17149, 6247, 13259, 15162, 5095, 5753, 10463, 18487,
        14919, 1410, 14615, 15292, 354, 12161, 7012, 9812, 7208, 15509,
        18623, 13059, 13788, 178, 15308, 7030, 18424, 5961, 812, 15930,
        12497, 5529, 3184, 2, 17845, 15825, 4803, 10793, 7347, 16886, 4218,
        2796, 7682, 17617, 7726, 4862, 16407, 7465, 10390, 18039, 4172,
        13383, 17928, 10103, 18845, 4728, 18481, 7705, 11105, 637, 3846,
        12026, 13049, 8400, 3459, 14433, 2151, 18793, 10436, 14872, 2318,
        1977, 1507, 5670, 7632, 8132, 16351, 5640, 605, 9724, 17815, 9124,
        5096, 18819, 6914, 18153, 16741, 142, 16512, 9602, 18148, 13659,
        17901, 2636, 6377, 13068, 6952, 5294, 16761, 5339, 10067, 879,
        5933, 8335, 18318, 557, 754, 13051, 13754, 15458, 12653, 17995,
        3000, 3019, 9037, 759, 7100, 15045, 11010, 12311, 11215, 11737,
        6472, 17557, 2561, 2906, 12904, 857, 5687, 10762, 4788, 10849,
        16804, 17442, 18426, 11618, 18297, 4217, 12484, 9031, 3143, 13669,
        16053, 7352, 6372, 8844, 3725, 18187, 8522, 3287, 528, 13929,
        13595, 10867, 23, 696, 7028, 3761, 8396, 1237, 3621, 7937, 18091,
        17860, 10896, 313, 2538, 14743, 9802, 13602, 17987, 17013, 12220,
        2590, 9490, 13543, 17923, 2179, 12707, 3306, 7613, 6704, 15564,
        4462, 4357, 14180, 18739, 8259, 875, 1991, 3066, 11690, 270, 18442,
        14539, 8329, 17480, 3614, 17110, 15641, 9816, 1710, 5365, 12010,
        15143, 13803, 16488, 6663, 5052, 9292, 1552, 2513, 9557, 13551,
        14842, 14621, 3, 2197, 9767, 14848, 12857, 7907, 5227, 4903, 790,
        15271, 11912, 296, 5953, 18927, 15734, 2663, 4488, 3631, 16100,
        285, 2198, 7019, 11263, 730, 3498, 10944, 14199, 14302, 10196,
        7780, 2711, 3385, 11441, 15264, 18632, 854, 10095, 12238, 14878,
        10582, 18569, 3488, 16582, 15465, 6698, 5234, 15907, 3150, 8711,
        14181, 7957, 5744, 9745, 7473, 15261, 16708, 12933, 4506, 9377,
        18850, 327, 14840, 9057, 7519, 10738, 11905, 17429, 12438, 5332,
        2038, 14742, 9859, 13424, 13475, 16739, 1276, 9941, 8603, 3557,
        7407, 9414, 11247, 14409, 245, 10244, 14029, 2566, 2101, 17564,
        1215, 9098, 11270, 17861, 3946, 10828, 11948, 17533, 1071, 9108
    ]
    assert len(posts) == 948
    post_tags = []
    with open('sentiment.log', 'w') as file:
        for idx, post in enumerate(posts):
            os.system('cls' if os.name == 'nt' else 'clear')
            print('#########################', idx, '#########################', flush=True)
            print(Post.get(Post.id == post).message, flush=True)
            while True:
                tag = input('[sentiment.py] Input (P)ositive or (N)egative: ')
                if tag == 'p' or tag == 'P':
                    file.write('post_tags[' + str(idx) + '] = \'pos\'\n')
                    post_tags.append('pos')
                    break
                elif tag == 'n' or tag == 'N':
                    file.write('post_tags[' + str(idx) + '] = \'neg\'\n')
                    post_tags.append('neg')
                    break
            file.flush()
            os.fsync(file.fileno())
    os.system('cls' if os.name == 'nt' else 'clear')
    assert len(post_tags) == 948
    accuracy_of_folds = []
    for i in range(10):
        prepare(posts[:i*95] + posts[(i+1)*95:], post_tags[:i*95] + post_tags[(i+1)*95:])
        accuracy = validate(posts[i*95:(i+1)*95], post_tags[i*95:(i+1)*95])
        print('Accuracy of fold ' + str(i+1) + ': ' + str(accuracy) + '%')
        accuracy_of_folds.append(accuracy)
    average_accuracy = sum(accuracy_of_folds) / len(accuracy_of_folds)
    print('Average accuracy: ' + str(average_accuracy) + '%')
    prepare(posts, post_tags)

if __name__ == '__main__':
    # init()
    ten_fold_cross_validation()
    # insert()
