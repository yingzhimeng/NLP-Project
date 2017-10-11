import nltk
import collections
import re


def get_trainTokens(file):
    text = ''
    f = open(file)
    all_tokens = []
    text = text.replace('. ', '. START ')
    all_tokens = nltk.word_tokenize(f.read().decode('utf-8'))
    f.close()
    return all_tokens

#english
en_Tokens = get_trainTokens('HW2english.txt')
en_Bigrams = [(en_Tokens[i],en_Tokens[i+1]) for i in xrange(len(en_Tokens)-1)]
en_Bigrams_map = collections.Counter(en_Bigrams)
en_unigrams_map = collections.Counter(en_Tokens)
en_len = len(en_unigrams_map)
#french
fr_Tokens = get_trainTokens('HW2french.txt')
fr_Bigrams = [(fr_Tokens[i],fr_Tokens[i+1]) for i in xrange(len(fr_Tokens)-1)]
fr_Bigrams_map = collections.Counter(fr_Bigrams)
fr_unigrams_map = collections.Counter(fr_Tokens)
fr_len = len(fr_unigrams_map)
#german
gr_Tokens = get_trainTokens('HW2german.txt')
gr_Bigrams = [(gr_Tokens[i],gr_Tokens[i+1]) for i in xrange(len(gr_Tokens)-1)]
gr_Bigrams_map = collections.Counter(gr_Bigrams)
gr_unigrams_map = collections.Counter(gr_Tokens)
gr_len = len(gr_unigrams_map)

def good_turing(tokens, map):
    p = []
    n = sum(map.values())
    for i in range(len(tokens)):
        c = map.get(tokens[i],0)
        if c == 0:
            n1 = n
        else:
            n1 = sum([j[1] for j in map.iteritems() if j[1] == c])
        n2 = sum([j[1] for j in map.iteritems() if j[1] == c+1])
        p.append((c+1.0)*n2/n1)

    return reduce(lambda x, y: x + y, p)


f = open('LangID.test.txt')
test = f.read().decode('utf-8')
test = test.split('\r')
for line in range(len(test)):
    test[line] = re.sub(r'[^\w\s]|[\d+]', '', test[line], re.UNICODE)  

res = []
for line in test:
    tokens = nltk.word_tokenize(line)
    bigrams = [(tokens[i], tokens[i+1]) for i in xrange(len(tokens)-1)]

    score_en = good_turing(tokens,en_unigrams_map)
    score_fr = good_turing(tokens,fr_unigrams_map)
    score_gr = good_turing(tokens,gr_unigrams_map)
    lan = {0:'unknow',score_en:'EN',score_fr:'FR',score_gr:'GR'}[max(score_en,score_fr,score_gr)]
    res.append(lan)
   
    
print res   
print len(res)
f = open('BigramWordLangId-GT.out', 'w')

for i in range(len(res)):
    f.write(str(i+1)+'. ' + res[i]+'\n')
f.close()