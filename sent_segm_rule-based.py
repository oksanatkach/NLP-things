INDICS = ['.', '!', '?', '...']

fh = open('custom_input.txt', 'r')
text = fh.read()

sents = []
for char in text:
    if char in INDICS:
        sent = text[:text.index(char)+1]
        text = text[text.index(char)+1:]
        sents.append(sent.strip())

for sent in sents:
    if sent.startswith('"') or sent.startswith('\''):
        if sent[1].isupper():
            next_sent = sents[sents.index(sent)+1]
            print sent + next_sent
            sents.remove(sent)
            sents.remove(next_sent)

for sent in sents:
    print sent