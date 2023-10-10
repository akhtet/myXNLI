
import sys
from nltk.translate import bleu_score
from sylbreak3 import *

reference = 'output/my/my.genre.test.tsv'
candidate = 'output/my/my.bleu.test.tsv'

if __name__ == '__main__':
    """
    USAGE: python script/get-bleu-my-test.py [limit]
    """

    if len(sys.argv) > 1:
        limit = int(sys.argv[1])
        print("Limiting to %d" % limit)
    else:
        limit = -1 # 0.5173

    translations = {}

    with open(reference, 'r', encoding='utf-8') as f:
        f.readline() # skip header
        reference_lines = f.readlines()
        counter = 0
        for line in reference_lines:
            cols = line.strip().split('\t')
            sentence1_en = cols[2]
            sentence2_en = cols[3]
            sentence1_my = cols[4]
            sentence2_my = cols[5]
            
            # Tokenize the translations
            translations[sentence1_en] = {'ref': sylbreak(sentence1_my).split(' ')}
            translations[sentence2_en] = {'ref': sylbreak(sentence2_my).split(' ')}
            
            counter += 1
            if limit > 0 and counter == limit: 
                break
            
    with open(candidate, 'r', encoding='utf-8') as f:
        f.readline() # skip header
        candidate_lines = f.readlines()
        counter = 0
        for line in candidate_lines:
            cols = line.strip().split('\t')
            sentence1_my = cols[1]
            sentence2_my = cols[2]
            sentence1_en = cols[3]
            sentence2_en = cols[4]
            translations[sentence1_en]['can'] = sylbreak(sentence1_my).split(' ')
            translations[sentence2_en]['can'] = sylbreak(sentence2_my).split(' ')

            counter += 1
            if limit > 0 and counter == limit: 
                break

    assert len(reference_lines) == len(candidate_lines)

    input(f"There are %d translations. Press ENTER to proceed:" % len(translations.keys()))

    references = []
    candidates = []

    for k in translations.keys():

        print ("%s\n\tR:%s\n\tC:%s\n" % (k, translations[k]['ref'], translations[k]['can']))
        
        # https://stackoverflow.com/questions/62337356/bleu-error-n-gram-overlaps-of-lower-order
        references.append([translations[k]['ref']])
        candidates.append(translations[k]['can'])
    
    #https://www.nltk.org/api/nltk.translate.bleu_score.html#nltk.translate.bleu_score.corpus_bleu
    print('BLEU score: {}'.format(bleu_score.corpus_bleu(references, candidates)))