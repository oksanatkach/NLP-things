#!/bin/python

import sys
import string
import operator


s = 'I came from the moon. He went to the other room. She went to the drawing room.'
sents = s.split('.')

trigrams = {}
order = []

for sent in sents:
    sent = sent.translate(None, string.punctuation).lower().split()

    for ind in xrange(2, len(sent)):


        tri = ' '.join([sent[ind - 2], sent[ind - 1], sent[ind]])

        if tri in trigrams.keys():
            trigrams[tri] += 1
        else:
            trigrams[tri] = 1
            order.append(tri)

srtd = sorted(trigrams.items(), key=operator.itemgetter(1))
max_count = [tri for tri in srtd if tri[1] == srtd[-1][1]]
if max_count == 1:
    print max_count[0][0]
else:
    ind = len(order)
    for el in max_count:
        if order.index(el[0]) < ind:
            ind = order.index(el[0])
            answer = el[0]
    print(answer)
