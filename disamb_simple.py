from nltk import word_tokenize
from nltk import PorterStemmer
from string import punctuation
from unidecode import unidecode
import codecs
import numpy as np
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from random import shuffle

punctuation.replace("'", '')
punctuation.replace("`", '')
punctuation = punctuation + "``''"
stemmer = PorterStemmer()


# def preproc(text):
#     res = []
#     text = text.translate(None, punctuation)
#     words = text.lower().split()
#     for w in words:
#         w_spl = w.split('-')
#         for w in w_spl:
#             # res = res + w_spl
#             if w.replace('-','').replace('.','').replace(',','').replace('s','').replace(':','').replace('degn','').replace('degw','').replace('g','').replace('/','').isdigit():
#                 res.append('<NUM>')
#             else:
#                 res.append(w)
#     return res


def preproc(text):
    text = unidecode(unicode(text, encoding="utf-8"))
    res = []
    words = word_tokenize(text)
    for w in words:
        w_spl = w.split('-')
        for w in w_spl:
            if w.replace('-','').replace('.','').replace(',','').replace('s','').replace(':','').replace('degn','').replace('degw','').replace('g','').replace('/','').isdigit():
                res.append('<NUM>')
            elif w not in punctuation:
                res.append(stemmer.stem(w))
    return res


def get_data(filename):
    text = open(filename, 'r').read().strip()
    return preproc(text)



def ctx(words, label):
    ALL = []
    for ind in xrange(len(words)):
        if 'apple' in words[ind]:
            ALL.append((words[ind - 5:ind] + words[ind+1:ind+6], label))
    return ALL


def vectorize(ALL, vocab):
    l = len(ALL)
    v_l = len(vocab)
    X = np.zeros((l, v_l))
    y = np.zeros((l))

    for ind in xrange(l):
        vec = np.zeros((v_l))
        for w in ALL[ind][0]:
            if w in vocab:
                vec[vocab.index(w)] = 1
        X[ind] = vec
        y[ind] = ALL[ind][1]

    return X, y

def predict(model, s, vocab):
    s = preproc(s)
    s_ctx = ctx(s, -1)
    x, _ = vectorize(s_ctx, vocab)
    return np.mean(model.predict(x))


if __name__ == '__main__':
    comp_words = get_data('apple-computers.txt')
    fruit_words = get_data('apple-fruit.txt')

    ALL = ctx(comp_words, 0) + ctx(fruit_words, 1)

    vocab = list( set( [ el for tpl in ALL for el in tpl[0] ] ) )

    shuffle(ALL)
    X, y = vectorize(ALL, vocab)

    clf = LogisticRegression()
    clf.fit(X, y)

    inp = open('input00.txt', 'r').read().strip().split('\n')[1:]
    outp = open('output00.txt', 'r').read().strip().split('\n')

    for ind in xrange(len(inp)):
        pred = predict(clf, inp[ind], vocab)
        if pred < 0.5:
            print 'computer-company'
        else:
            print 'fruit'
