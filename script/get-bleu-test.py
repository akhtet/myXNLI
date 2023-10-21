
import sys
from nltk.translate import bleu_score
from sylbreak3 import *

if __name__ == '__main__':
    """
    USAGE: python script/get-bleu-sw-test.py [lang] [limit]
    """ 

    lang = sys.argv[1]
    reference = f'output/{lang}/{lang}.genre.test.tsv'
    candidate = f'output/{lang}/{lang}.bleu.test.tsv'

    if len(sys.argv) > 2:
        limit = int(sys.argv[2])
        print("Limiting to %d" % limit)
    else:
        limit = -1 
        # my: 0.5173
        # ur: 0.2373
        # sw: 0.2905
        # BLEU score of over 50 may be considered good quality 
        # https://cloud.google.com/translate/automl/docs/evaluate

    tokenize = lambda x: sylbreak(x).split(' ') if lang == 'my' else x.split(' ')

    translations = {}

    # This assumes that the reference and candidate files are in the same order.
    with open(reference, 'r', encoding='utf-8') as rf:
        with open(candidate, 'r', encoding='utf-8') as cf:
            rf.readline() # skip header
            cf.readline() # skip header
            reference_lines = rf.readlines()
            candidate_lines = cf.readlines()
           
            max_limit = limit if limit > 0 else len(reference_lines)

            for i in range(0, max_limit):
                r_cols = reference_lines[i].strip().split('\t')
                r_sentence1 = r_cols[-2]
                r_sentence2 = r_cols[-1]
          
                c_cols = candidate_lines[i].strip().split('\t')
                c_sentence1 = c_cols[1]
                c_sentence2 = c_cols[2]

                # Tokenize the translations
                for (r,c) in [(r_sentence1, c_sentence1), (r_sentence2, c_sentence2)]:
                    if r not in translations:
                        translations[r] = {'ref': tokenize(r), 'can': tokenize(c)}

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