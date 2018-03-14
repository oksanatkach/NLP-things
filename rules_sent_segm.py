import re

TERMIN = ['.','!','?']
ABBR = ['Dr.', 'Esq.', 'Hon.', 'Jr.', 'Mr.', 'Mrs.', 'Ms.', 'Messrs.', 'Mmes.', 'Msgr.', 'Prof.', 'Rev.', 'Rt.', 'Hon.', 'Sr.', 'St.']

in_txt = raw_input()


def preproc(text):
    words = text.split()
    new_words = []
    # Check if whitespace missed
    for ind in range(len(words)):
        if re.search('(\.\.\.|\?|\.|!)([A-Z])', words[ind]):
            spl = re.search('(.*?)(\.\.\.|\?|\.|!)(.*)', words[ind])
            new_words.append(''.join(spl.group(1, 2)))
            new_words.append(spl.group(3))
        else:
            new_words.append(words[ind])
    return new_words


def find_sent(words, sents):

    for ind in range(len(words)):
        word = words[ind]

        # Check if end of text
        if ind == len(words)-1:
            sent = ' '.join(words)
            sents.append(sent)
            return sents

        # Handle quotes
        elif words[ind].startswith('"'):
            quend = words.index(next(word for word in words[1:] if word.endswith('"')))
            if words[quend][-2] in TERMIN and words[ind+1][0].isupper():
                sent = ' '.join(words[:quend+1])
                sents.append(sent)
                words = words[quend+1:]
                return find_sent(words, sents)

        elif words[ind] not in ABBR and words[ind][-1] in TERMIN and words[ind+1][0].isupper() or words[ind+1].startswith('"'):
            sent = ' '.join(words[:ind+1])
            sents.append(sent)
            words = words[ind+1:]
            return find_sent(words, sents)

sents = find_sent(preproc(in_txt), [])

for sent in sents:
    print(sent)
