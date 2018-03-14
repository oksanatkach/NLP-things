import re
from nltk import word_tokenize
import nltk
from nltk.corpus import brown

TERMIN = ['.','!','?']

honourific_list = [
	"mr.",
	"mrs.",
	"dr.",
	"drs.",
	"ms.",
	"prof.",
	"profs.",
	"pvt.",
	"pvts.",
	"cpl.",
	"cpls.",
	"mcpl.",
	"mcpls.",
	"sgt.",
	"sgts.",
	"wo.",
	"wos.",
	"cdt.",
	"ctds.",
	"lt.",
	"lts.",
	"cpt.",
	"capt.",
	"cpts.",
	"capts.",
	"mjr.",
	"mjrs.",
	"col.",
	"cols.",
	"gen.",
	"gens.",
	"hrm.",
	"hrms.",
	"rep.",
	"reps.",
	"rev.",
	"revs.",
	"sen.",
	"sens.",
	"jr.",
	"sr."
]

month_list = [
	"jan.",
	"feb.",
	"mar.",
	"apr.",
	"jun.",
	"jul.",
	"aug.",
	"sept.",
	"oct.",
	"nov.",
	"dec."
]

abbreviation_list = [
	"fig.",
	"figs.",
	"s.",
	"st.",
	"ave.",
	"pp.",
	"pg.",
	"no.",
	"gov.",
	"p.m.",
	"a.m.",
	"cc.",
	"inc.",
	"co.",
	"i.d.",
	"cf.",
	"ch.",
	"vs.",
	"h.m.s.",
	"lb.",
	"lbs.",
	"p.",
	"m.p.h.",
	"in.",
	"stat.",
	"dept.",
	"e.g."
]



country_list = [
	"u.s."
]

day_list = [
	"mon.",
	"tues.",
	"wed.",
	"thurs.",
	"fri.",
	"sat.",
	"sun."
]

state_list = [
	"ala.",
	"ariz.",
	"ark.",
	"calif.",
	"colo.",
	"conn.",
	"del.",
	"fla.",
	"ga.",
	"ill.",
	"ind.",
	"kans.",
	"ky.",
	"la.",
	"md.",
	"mass.",
	"mich.",
	"minn.",
	"miss.",
	"mo.",
	"mont.",
	"nebr.",
	"n.h.",
	"n.j.",
	"n.m.",
	"n.y.",
	"n.c.",
	"n.d.",
	"okla.",
	"ore.",
	"pa.",
	"r.i.",
	"s.c.",
	"s.d.",
	"tenn.",
	"tex.",
	"vt.",
	"va.",
	"wash.",
	"w.va.",
	"wis.",
	"wyo."
]

ABBR = honourific_list + month_list +\
               abbreviation_list + day_list +\
               country_list + state_list

text = open('input.txt','r').read()
words = word_tokenize(text)


def iscap(word):
    try:
        return word[0].isupper()
    except:
        return False


def gen_feats(prv, cur, nxt):
    feats = {}

    feats['f1'] = iscap(prv)
    feats['f2'] = iscap(nxt)
    feats['f3'] = prv.isupper()
    feats['f4'] = len(prv)
    feats['f5'] = len(nxt)
    feats['f6'] = cur in [':','--','...']
    feats['f7'] = nxt == '$'
    feats['f8'] = nxt.replace('.','').replace('-','').isdigit()
    feats['f9'] = prv in ABBR
    feats['f10'] = cur in TERMIN and nxt == '``'
    feats['f11'] = cur in TERMIN and nxt != '``'
    feats['f12'] = prv in TERMIN and cur in ["'", '"'] and nxt == '``' or iscap(nxt)

    return feats

sents = brown.sents()

def prep_feats(sents):
	data = []
	for sent in sents:
		for ind in xrange(len(sent)):
			label = 'n'
			if ind == 0:
				prv = ''
			else:
				prv = sent[ind-1]
			cur = sent[ind]
			if ind == len(sent)-1:
				nxt = ''
				label = 'y'
			else:
				nxt = sent[ind+1]
			data.append((gen_feats(prv, cur, nxt), label))
	return data

train = prep_feats(sents[:1000])
# train = prep_feats(sents[:100])

classifier = nltk.classify.maxent.MaxentClassifier.train(train, 'GIS', trace=0, max_iter=50)

def find_sent(words, sents):

	for ind in xrange(len(words)):

		if ind == len(words) - 1:
			sent = ' '.join(words)
			sents.append(sent)
			return sents
		else:
			if ind == 0:
				prv = ''
			else:
				prv = words[ind-1]
			cur = words[ind]
			if ind == len(words)-1:
				nxt = ''
			else:
				nxt = words[ind+1]
			if classifier.classify((gen_feats(prv, cur, nxt))) == 'y':
				sent = ' '.join(words[:ind + 1])
				sents.append(sent)
				words = words[ind + 1:]
				return find_sent(words, sents)

sents = find_sent(words, [])
print len(sents)
for sent in sents:
	sent = sent.replace('( ','(').replace(' )',')')
	sent = sent.replace(' ,',',')
	sent = sent.replace(' .','.')
	sent = sent.replace(' \'','\'')
	sent = sent.replace(' ?','?')
	sent = sent.replace(' !','!')
	sent = sent.replace('\'\' ','\'\'')
	# sent = sent.replace(' \'\'','\'\'')
	sent = sent.replace('`` ','``')
	print sent
