import string
from collections import defaultdict
import operator


class Trie:

    def __init__(self):
        self.root = defaultdict()

    def show(self):
        print self.root

    def insert(self, word):
        current = self.root
        for letter in word:
            current = current.setdefault(letter, {})
        current.setdefault("_end")

    def search(self, word):
        current = self.root
        for letter in word:
            if letter not in current:
                return False
            current = current[letter]
        if "_end" in current:
            return True
        return False

    def startsWith(self, prefix):
        current = self.root
        for letter in prefix:
            if letter not in current:
                return False
            current = current[letter]
        return True


def gen_trie(words):
    trie = Trie()
    for word in words:
        trie.insert(word)
    return trie


def gen_counts(dict, corp):
    counts = {w:1 for w in dict}
    for w in corp:
        try:
            counts[w] += 1
        except:
            continue
    return counts


def find_starts(s):
    cands = vals[int(s[0])]
    for ind in xrange(1, len(s)):
        temp = []
        for char in vals[int(s[ind])]:
            for segm in cands:
                if trie.startsWith(segm+char):
                    temp.append(segm+char)
        cands = temp
    return cands


def top5(s, counts):
    starts = find_starts(s)
    if starts == []:
        return 'No Suggestions'
    else:
        out = []
        for word in dict:
            if word[:len(s)] in starts:
                w_count = counts[word]
                if len(out) == 0:
                    out.append((word, w_count))
                else:
                    bigger = False
                    for ind in xrange(len(out)):
                        if out[ind][1] < w_count:
                            out = out[:ind] + [(word, w_count)] + out[ind:]
                            bigger = True
                            break
                    if not bigger:
                        out.append((word, w_count))
                        out = out[:5]
        return ';'.join([val[0] for val in out])


inp = open('T9input.txt', 'r').read().split('\n')[1:]
dict = open('t9Dictionary.txt', 'r').read().split('\n')[1:]
corp = open('t9TextCorpus.txt', 'r').read().lower()
punct = string.punctuation
punct = punct.replace("'", '')
corp = corp.translate(None, punct)
corp = corp.split()

vals = {0:[], 1:[], 2:['a','b','c'], 3:['d','e','f'],
        4:['g','h','i'], 5:['j','k','l'],
        6:['m','n','o'], 7:['p','q','r','s'],
        8:['t','u','v'], 9:['w','x','y','z']}

trie = gen_trie(dict)
counts = gen_counts(dict, corp)

# for s in inp:
#     print top5(s, counts)
print top5('58624',counts)
# print counts['lunched']
# print counts['lunching']
# print counts['lunchtime']
