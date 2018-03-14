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
    text = open(filename, 'r').read().strip().lower()
    return preproc(text)


def one_hot(words, vocab, label):
    ALL = []
    vec_l = len(vocab)
    for ind in xrange(len(words)):
        if 'appl' in words[ind]:
            vec = [0]*vec_l
            ctx = words[ind - 5:ind] + words[ind+1:ind+6]
            for w in ctx:
                if w != '<PAD>' and w in vocab:
                    vec[vocab.index(w)] = 1
            ALL.append((vec, label))
    return ALL


def prep_xy(ALL, shape):
    X = np.ndarray(shape)
    y = np.ndarray(shape[0])

    for ind in xrange(shape[0]):
        X[ind] = ALL[ind][0]
        y[ind] = ALL[ind][1]

    return X, y

def predict(model, s, vocab):
    s = preproc(s)
    x = one_hot(s, vocab, '_')
    x = np.array([x[0][0]])
    return model.predict(x).tolist()


if __name__ == '__main__':
    comp_words = get_data('apple-computers.txt')
    fruit_words = get_data('apple-fruit.txt')
    vocab = list(set(comp_words + fruit_words))

    ALL = one_hot(comp_words, vocab, 0) + one_hot(fruit_words, vocab, 1)
    shuffle(ALL)
    X, y = prep_xy(ALL, (len(ALL), len(vocab)))

    clf = LogisticRegression()
    clf.fit(X, y)

    inp = open('input00.txt', 'r').read().strip().split('\n')[1:]
    outp = open('output00.txt', 'r').read().strip().split('\n')

    for ind in xrange(len(inp)):
        print ind
        print predict(clf, inp[ind], vocab)
        print outp[ind]
