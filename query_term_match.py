import string
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

punct = string.punctuation.replace('-', '')
stop = set(stopwords.words('english'))
stemmer = PorterStemmer()

def preproc(s):
    res = []
    words = set(s.translate(None, punct).lower().split())
    for word in words:
        if not word.isdigit() and not word in stop:
            if '-' in word:
                word_spl = word.split('-')
                for w in word_spl:
                    res.append(stemmer.stem(w))
            else:
                res.append(stemmer.stem(word))
    return set(res)


def gen_classes(keys):
    classes = {}
    for cl in keys:
        classes[cl] = preproc(cl)
    return classes


if __name__ == '__main__':
    training = open('training.txt', 'r').read().strip().split('\n')[1:]
    inp = open('sampleInput.txt','r').read().strip().split('\n')[1:]
    outp = open('sampleOutput.txt','r').read().strip().split('\n')

    tr_dict = {}
    for s in training:
        s = s.split('\t')
        if s[1] in tr_dict.keys():
            tr_dict[s[1]].append(s[0])
        else:
            tr_dict[s[1]] = [s[0]]

    classes = gen_classes(tr_dict.keys())

    # for ind in xrange(len(inp)):
        # s = preproc('Nike Up or Down Deodorant Spray  -  200 ml (For Men)')
    s = preproc('Laptops: AMD Mobile Platform, AMD Vision, Barebook, Cen...')
    res = {}
        # inters = 0

    for cl in classes:
        cl_inters = len(s.intersection(classes[cl]))
        if cl_inters > 0:
            res[cl] = cl_inters
    print res
            # if cl_inters > inters:
            #     resp = cl
            #     inters = cl_inters
        # if resp != outp[ind]:
        #     print inp[ind] + '\t' + outp[ind] + '\t' + resp
