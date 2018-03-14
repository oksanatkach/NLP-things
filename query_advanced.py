import random
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer


def model(X, y):
    return LogisticRegression(C=1).fit(X, y)


def predict(model, x, classes):
    ind = int(model.predict(x).tolist()[0])
    return classes[ind]


def get_data(training, vectorizer):
    strings = []
    labels = []
    for line in training:
        line = line.split('\t')
        strings.append(line[0])
        labels.append(line[1])
    unique = list(set(labels))
    return vectorizer.fit_transform(strings),\
           [unique.index(l) for l in labels],\
           unique


if __name__ == '__main__':

    training = open('training.txt', 'r').read().strip().split('\n')[1:]
    random.shuffle(training)

    vectorizer = TfidfVectorizer(
                    ngram_range=(1, 5),
                    stop_words='english',
                    analyzer='char',
                    max_df=0.5
                    )

    X, y, classes = get_data(training, vectorizer)
    model = model(X, y)

    inp = open('sampleInput.txt', 'r').read().strip().split('\n')[1:]
    s = inp[0]
    print s
    x = vectorizer.transform([s])
    print predict(model, x, classes)
