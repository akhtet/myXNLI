
import sys, random

from nltk.translate import bleu_score

reference = 'output/my/my.genre.test.tsv'
candidate = 'output/my/raw.myxnli.bleu.test.tsv'

if __name__ == '__main__':

    translations = {}

    with open(reference, 'r', encoding='utf-8') as f:
        f.readline() # skip header
        reference_lines = f.readlines()
        for line in reference_lines:
            cols = line.strip().split('\t')
            sentence1_en = cols[2]
            sentence2_en = cols[3]
            sentence1_my = cols[4]
            sentence2_my = cols[5]
            #TODO Tokenize the translations
            translations[sentence1_en] = {'ref': sentence1_my}
            translations[sentence2_en] = {'ref':sentence2_my}
            
            
    with open(candidate, 'r', encoding='utf-8') as f:
        f.readline() # skip header
        candidate_lines = f.readlines()
        for line in candidate_lines:
            cols = line.strip().split('\t')
            sentence1_my = cols[1]
            sentence2_my = cols[2]
            sentence1_en = cols[3]
            sentence2_en = cols[4]
            translations[sentence1_en]['can'] = sentence1_my
            translations[sentence2_en]['can'] = sentence2_my

    assert len(reference_lines) == len(candidate_lines)

    input(f"There are %d translations" % len(translations.keys()))

    references = []
    candidates = []

    for k in translations.keys():

        print ("%s\n\t%s\n\t%s" % (k, translations[k]['ref'], translations[k]['can']))
        references.append(translations[k]['ref'])
        candidates.append(translations[k]['can'])

    print('BLEU score: {}'.format(bleu_score.corpus_bleu(references, candidates)))