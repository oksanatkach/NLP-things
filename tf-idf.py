import string
import nltk
from math import log
import operator

doc1 = "I'd like an apple."
doc2 = "An apple a day keeps the doctor away."
doc3 = "Never compare an apple to an orange."
doc4 = "I prefer scikit-learn to orange."

def preproc(doc):
    doc = doc.lower()
    doc = nltk.word_tokenize(doc)
    return doc

def tf(t, d):
    return d.count(t)

def idf(t, D):
    return log(float(len(D)) / len([d for d in D if t in d]))

def tf_idf(vocab, d, D):
    scores = []
    for t in vocab:
        scores.append(tf(t, d) * idf(t, D))
    return scores

def similarity(target, scores, vocab):
    scores.pop(' '.join(target))
    sims = {doc:0 for doc in scores.keys()}
    for doc in scores:
        for word in target:
            ind = vocab.index(word)
            sims[doc] += scores[doc][ind]
    return max(sims.iteritems(), key=operator.itemgetter(1))[0]


D = [preproc(doc) for doc in [doc1,doc2,doc3,doc4]]

vocab = set([word for doc in D for word in doc])

scores = {' '.join(d) : tf_idf(vocab, d, D) for d in D}

target = preproc(doc1)

print similarity(target, scores, list(vocab))
