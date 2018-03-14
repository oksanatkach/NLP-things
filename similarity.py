from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as calc_cos_sim

text = open('input00.txt', 'r').read().strip()
N = text[0]
sets = text[2:].split('*****')
A = sets[0].strip().split('\n')
B = sets[1].strip().split('\n')

vectorizer = TfidfVectorizer(
                            ngram_range=(1,5),
                            stop_words='english',
                            analyzer='char',
                            max_df=0.5
                            )

vectorizer.fit(A+B)
A_vec = vectorizer.transform(A)
B_vec = vectorizer.transform(B)

res = []
for doc in A:
    a = vectorizer.transform([doc])
    res.append([calc_cos_sim(a, b).tolist()[0][0] for b in B_vec])


def check_other(max_ind, max_score, scores):
    for other_scores in res:
        if other_scores[max_ind] > max_score:
            working = list(scores)
            working.remove(max_score)
            max_score = max(working)
            return scores.index(max_score)
    else:
        return max_ind

for scores in res:
    max_score = max(scores)
    max_ind = scores.index(max_score)
    working_scores = list(scores)
    print check_other(max_ind, max_score, scores) + 1
