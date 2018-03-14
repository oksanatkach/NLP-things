import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as calc_cos_sim

t = time.time()

text = open('query_input.txt', 'r').read().strip()
N = text[0]
sets = text[2:].split('*****')
A = sets[0].strip().split('\n')
B = sets[1].strip().split('\n')

vectorizer = TfidfVectorizer(
    #ngram_range=(1, 3),
    stop_words='english',
    analyzer='char',
    max_df=0.5
)

vectorizer.fit(A + B)

A_vec = vectorizer.transform(A)
B_vec = vectorizer.transform(B)

for b in B_vec:
    scores = [calc_cos_sim(a, b).tolist()[0][0] for a in A_vec]
    print scores.index(max(scores))+1
print "Analyzed one: " + str(time.time()-t)
t = time.time()
