import nltk
import collections
import re


def get_trainTokens(file):
    text = ''
    f = open(file)
    all_tokens = []
    text = text.replace('. ', '. $ ')
    text = re.sub(r'[^\w\s]','',text, re.UNICODE)
    all_tokens = nltk.word_tokenize(f.read().decode('utf-8'))
    f.close()
    return all_tokens

#english
en_Tokens = get_trainTokens('HW2english.txt')
en_unigrams_map = collections.Counter(en_Tokens)
en_Bigrams = [(en_Tokens[i],en_Tokens[i+1]) for i in range(len(en_Tokens)-1)]
en_Bigrams_map = collections.Counter(en_Bigrams)
en_Trigrams = [(en_Tokens[i],en_Tokens[i+1], en_Tokens[i + 2]) for i in range(len(en_Tokens)-2)]
en_Trigrams_map = collections.Counter(en_Trigrams)
en_len = len(en_unigrams_map)
#french
fr_Tokens = get_trainTokens('HW2french.txt')
fr_unigrams_map = collections.Counter(fr_Tokens)
fr_Bigrams = [(fr_Tokens[i],fr_Tokens[i+1]) for i in range(len(fr_Tokens)-1)]
fr_Bigrams_map = collections.Counter(fr_Bigrams)
fr_Trigrams = [(fr_Tokens[i],fr_Tokens[i+1],fr_Tokens[i + 2]) for i in range(len(fr_Tokens)-2)]
fr_Trigrams_map = collections.Counter(fr_Trigrams)
fr_len = len(fr_unigrams_map)
#german
gr_Tokens = get_trainTokens('HW2german.txt')
gr_unigrams_map = collections.Counter(gr_Tokens)
gr_Bigrams = [(gr_Tokens[i],gr_Tokens[i+1]) for i in xrange(len(gr_Tokens)-1)]
gr_Bigrams_map = collections.Counter(gr_Bigrams)
gr_Trigrams = [(gr_Tokens[i],gr_Tokens[i+1], gr_Tokens[i + 2]) for i in range(len(gr_Tokens)-2)]
gr_Trigrams_map = collections.Counter(gr_Trigrams)
gr_len = len(gr_unigrams_map)

def backoff(trigrams, BigramsDic, TrigramsDic, Dic, V):
    res = 1.0
    for i in range(len(trigrams)):
        p1 = (TrigramsDic.get(trigrams[i], 0.0) + 1.0)/(BigramsDic.get((trigrams[i][0],trigrams[i][1]), 0.0) + 4000)
        p2 = (BigramsDic.get((trigrams[i][0],trigrams[i][1]), 0.0) + 1.0)/(Dic.get(trigrams[i][0], 0.0) + 4000)
        p3 = (Dic.get(trigrams[i][0], 0.0) + 1.0)/ (2*4000)
        res *= 0.6*p1+0.2*p2+0.2*p3
    return res

f = codecs.open('LangID.test.txt', encoding = 'utf-8')
test = f.readlines()

for i in range(len(test)):
    test[i] = re.sub(r'[^\w\s] | \d+', '', test[i], re.UNICODE)

res = []
for l in test:
    tokens = nltk.word_tokenize(l)
    trigrams = [(tokens[i], tokens[i + 1], tokens[i + 2]) for i in xrange(len(tokens) - 2)]

    score_en = backoff(trigrams, en_Bigrams_map, en_Trigrams_map, en_unigrams_map, en_len)
    score_fr = backoff(trigrams, fr_Bigrams_map, fr_Trigrams_map, fr_unigrams_map, fr_len)
    score_gr = backoff(trigrams, gr_Bigrams_map, gr_Trigrams_map, gr_unigrams_map, gr_len)
    lan = {0:'unknow',score_en:'EN',score_fr:'FR',score_gr:'GR'}[max(score_en,score_fr,score_gr)]
#     lan = 'UNK'
#     if score_en > score_fr and score_en > score_gr:
#         lan = 'EG'
#     else:
#         if score_fr > score_en and score_fr > score_gr:
#             lan = 'FR'
#         else:
#             lan = 'GR'
    res.append(lan)
    print lan
f = open('BigramWordLangId-KBO.out', 'w')
for i in range(len(res)):
    f.write(str(i+1)+'. ' + res[i]+'\n')
f.close()


