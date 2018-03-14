from collections import defaultdict


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


def preproc(in_str):
    if in_str.startswith('#'):
        return in_str[1:]
    elif in_str.startswith('www.'):
        in_str = in_str[4:]
    in_str = in_str.split('.')
    return in_str[0]


def find_words(s, trie):
    res = []
    stack = []
    start = 0
    end = 1
    while end < len(s)+1:
        cand = s[start:end]

        if cand.replace('.','').isdigit():
            if ( end != len(s) and not s[end].isdigit() ) or end == len(s):
                res.append(cand)
                stack.append(end)
            end += 1

        elif trie.startsWith(cand):
            if trie.search(cand):
                res.append(cand)
                stack.append(end)
            end += 1
        else:
            start = stack.pop()
            end = start + 1

        if end == len(s)+1:
            start = stack.pop()
            end = start+1

    return res


def choose_words(s, res):
    end = len(s)
    chosen = []

    while res and end >= 0:
        curWord = res.pop()
        start = end - len(curWord)

        if start >= 0:
            if s[start:end].startswith(curWord):
                chosen.append(curWord)
                end = start
        else:
            end = start + len(curWord)

    chosen.reverse()
    return ' '.join(chosen)

if __name__ == '__main__':
    words = list(set(open('words.txt', 'r').read().strip().lower().split()))
    trie = gen_trie(words)

    n = int(raw_input())
    for i in range(n):
        s = preproc(raw_input())
        print choose_words(s, find_words(s, trie))

    # inp = open('input04.txt', 'r').read().strip().lower().split('\n')[1:]
    # outp = open('output04.txt', 'r').read().strip().lower().split('\n')

    # for ind in xrange(len(inp)):
    #     s = preproc(inp[ind])
    #     true = outp[ind]
    #     pred = choose_words(s, find_words(s, trie))
    #     print s + '\t' + true + '\t' + pred

# https://github.com/sharat7j/HackerRank/blob/master/Deterministic%20url%20and%20Hashtag%20segmentation/SegmentWords.py
