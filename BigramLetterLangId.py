import nltk
import collections
import re
import string
import codecs
from nltk.util import ngrams

def get_trainTokens(file):
    text = ''
    f = open(file)
    text = f.read().decode('utf-8')
    text = re.sub(r'[^\w\s]','',text, re.UNICODE)
    all_tokens = []
    text = text.replace(' ', ' $')
    all_tokens = [word[i] for word in text.split(' ') for i in range(len(word))]
    f.close()
    return all_tokens

#english
en_Tokens = get_trainTokens('HW2english.txt')
en_Bigrams = [(en_Tokens[i],en_Tokens[i+1]) for i in range(len(en_Tokens)-1)]
en_Bigrams_map = collections.Counter(en_Bigrams)
en_unigrams_map = collections.Counter(en_Tokens)
#french
fr_Tokens = get_trainTokens('HW2french.txt')
fr_Bigrams = [(fr_Tokens[i],fr_Tokens[i+1]) for i in xrange(len(fr_Tokens)-1)]
fr_Bigrams_map = collections.Counter(fr_Bigrams)
fr_unigrams_map = collections.Counter(fr_Tokens)
#german
gr_Tokens = get_trainTokens('HW2german.txt')
gr_Bigrams = [(gr_Tokens[i],gr_Tokens[i+1]) for i in xrange(len(gr_Tokens)-1)]
gr_Bigrams_map = collections.Counter(gr_Bigrams)
gr_unigrams_map = collections.Counter(gr_Tokens)

def letter_bigrams(test_bigrams, bigrams_map, unigrams_map):
    scores = 1
    for bigram in test_bigrams:
        if bigram in bigrams_map:
            scores *= (bigrams_map[bigram] + 0.0) / unigrams_map[bigram[0]]
        else:
            scores *= 0.0
    return scores

f = open('LangID.test.txt')
test = f.read().decode('utf-8')
test = test.split('\r')
for line in range(len(test)):
    test[line] = re.sub(r'[^\w\s]|[\d+]', '', test[line], re.UNICODE)

res = []
for line in test:
    line = line.replace(' ', ' $')
    tokens = [word[i] for word in line.split(' ') for i in range(len(word))]
    bigrams = [(tokens[i], tokens[i+1]) for i in xrange(len(tokens)-1)]

    score_en = letter_bigrams(bigrams,en_Bigrams_map,en_unigrams_map)
    score_fr = letter_bigrams(bigrams,fr_Bigrams_map,fr_unigrams_map)
    score_gr = letter_bigrams(bigrams,gr_Bigrams_map,gr_unigrams_map)
    if score_en > score_fr and score_en > score_gr:
        lan = 'EG'
    if score_fr > score_en and score_fr > score_gr:
        lan = 'FR'
    if score_gr > score_fr and score_gr > score_en: 
        lan = 'GR'
    res.append(lan)
    
print len(res)

f = open('BigramLetterLangId.out', 'w')
for i in range(len(res)):
    f.write(res[i] + '\n')

f.close()