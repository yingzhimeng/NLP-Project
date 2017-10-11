import nltk
import collections
import re
import string
import codecs

def get_trainTokens(file):
    text = ''
    f = open(file)
    all_tokens = []
    text = text.replace('. ', '. START ')
    text = re.sub(r'[^\w\s]|[\d+]','',text, re.UNICODE)
    all_tokens = nltk.word_tokenize(f.read().decode('utf-8'))
    f.close()
    return all_tokens

#english
en_Tokens = get_trainTokens('HW2english.txt')
en_Bigrams = [(en_Tokens[i],en_Tokens[i+1]) for i in range(len(en_Tokens)-1)]
en_Bigrams_map = collections.Counter(en_Bigrams)
en_unigrams_map = collections.Counter(en_Tokens)
en_len = len(en_unigrams_map)
#french
fr_Tokens = get_trainTokens('HW2french.txt')
fr_Bigrams = [(fr_Tokens[i],fr_Tokens[i+1]) for i in range(len(fr_Tokens)-1)]
fr_Bigrams_map = collections.Counter(fr_Bigrams)
fr_unigrams_map = collections.Counter(fr_Tokens)
fr_len = len(fr_unigrams_map)
#german
gr_Tokens = get_trainTokens('HW2german.txt')
gr_Bigrams = [(gr_Tokens[i],gr_Tokens[i+1]) for i in range(len(gr_Tokens)-1)]
gr_Bigrams_map = collections.Counter(gr_Bigrams)
gr_unigrams_map = collections.Counter(gr_Tokens)
gr_len = len(gr_unigrams_map)

def word_bigrams(test_bigrams, bigrams_map, unigrams_map, V):
    scores = []
    for i in test_bigrams:
        scores.append((bigrams_map.get(i, 0.0) + 1.0) / ((unigrams_map.get(i[0], 0.0)) + V))
    return reduce(lambda x, y: x*y, scores)

f = open('LangID.test.txt')
test = f.read().decode('utf-8')
test = test.split('\r')
for line in range(len(test)):
    test[line] = re.sub(r'[^\w\s]|[\d+]', '', test[line], re.UNICODE)

res = []
for line in test:
    tokens = nltk.word_tokenize(line)
    bigrams = [(tokens[i], tokens[i+1]) for i in range(len(tokens)-1)]
    
    score_en = word_bigrams(bigrams,en_Bigrams_map,en_unigrams_map, 4000)
    score_fr = word_bigrams(bigrams,fr_Bigrams_map,fr_unigrams_map, 4000)
    score_gr = word_bigrams(bigrams,gr_Bigrams_map,gr_unigrams_map, 4000)
    
    lan = {0:'unknow',score_en:'EN',score_fr:'FR',score_gr:'GR'}[max(score_en,score_fr,score_gr)]
    res.append(lan)
    print lan
f = open('BigramWordLangId-AO.out', 'w')
print len(res)
for i in range(len(res)):
    f.write(str(i+1)+'. ' + res[i] + '\n')
f.close()