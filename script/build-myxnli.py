"""
Run this script from the main directory.
"""

import csv, sys, os, re

from validate import analyze_file

dev_file = 'xnli-original/xnli.dev.tsv'
test_file = 'xnli-original/xnli.test.tsv'
parallel_file = 'xnli-origin/xnli.15way.orig.tsv'

trans_dir = 'translation'
my_dev_file = 'output/my/my.genre.dev.tsv'
my_test_file = 'output/my/my.genre.test.tsv'

keyword_file = 'translation/keywords.csv'
en_sentence_file = 'translation/english.txt'

# Create DEV and TEST files from the Originals

BASIC_HEADER = ['label', 'sentence1_en', 'sentence2_en', 'sentence1_my', 'sentence2_my']
GENRE_HEADER = ['genre', 'label', 'sentence1_en', 'sentence2_en', 'sentence1_my', 'sentence2_my']

OUTPUT_FORMAT = 'GENRE' 


def build_dict():
    """
    Build a dictionary between EN and MY sentences 
    Summarises issues within each translation file   
    """
    my_dict = {}
    file_stats = {}
    debug_list = [] # Add file name to debug

    for fname in os.listdir(trans_dir):
        if not fname.startswith('my_'):
            continue

        print ('Processing', fname)   

        blocks, orphans, ratings = analyze_file(os.path.join(trans_dir, fname))
        for block_id in blocks:
            block = blocks[block_id]
            my_dict[block['source']] = block['target']                               
                       
            # if en_source in my_dict:
            #    print (fname, counter, state, line)
            #    raise Exception
                        
        file_stats[fname] = len(blocks)
    
    print ('%d entries loaded to the dictionary' % len(my_dict.keys()))
    return my_dict, file_stats


def write_source_sentences(my_dict):
    """
    Writes English sentences for NER task
    """
    print ('Writing ', en_sentence_file)
    outfile = open(en_sentence_file, 'wt', encoding='utf-8')
    for sent in my_dict:
        outfile.write(sent + '\n')
    outfile.close()


def write_dataset(my_dict):
    """
    Takes the original XNLI Dataset files and creates corresponding Burmese Dataset files
    Writes output files which can then be imported as MyXNLI Dataset
    """
    for infn, outfn in [(dev_file, my_dev_file), (test_file, my_test_file)]:
        with open(infn, encoding='utf-8') as infile:

            # Write the header
            print ('\nWriting ', outfn)
            outfile = open(outfn, 'wt', encoding='utf-8')

            if OUTPUT_FORMAT == 'BASIC':
                outfile.write('\t'.join(BASIC_HEADER) + '\n')
            elif OUTPUT_FORMAT == 'GENRE':
                outfile.write('\t'.join(GENRE_HEADER) + '\n')
            else:
                outfile.write(infile.readline())

            linenum = 0
            no_translation = []

            for line in infile.readlines():
                if line.startswith('en'):
                    linenum += 1
                    cols = line.split('\t')

                    # Column 7 and 8 are the unparsed English sentences
                    label = cols[1]
                    genre = cols[10]
                    sentence1 = cols[6]
                    sentence2 = cols[7]

                    if OUTPUT_FORMAT == 'BASIC':
                        out_cols = [
                            label,
                            sentence1,
                            sentence2,
                            my_dict.get(sentence1, sentence1),
                            my_dict.get(sentence2, sentence2)
                        ]

                    elif OUTPUT_FORMAT == 'GENRE':
                        out_cols = [
                            genre,
                            label,                         
                            sentence1,
                            sentence2,
                            my_dict.get(sentence1, sentence1),
                            my_dict.get(sentence2, sentence2)
                        ]

                        if sentence1 not in my_dict.keys():
                            no_translation.append(sentence1)
                        
                        if sentence2 not in my_dict.keys():
                            no_translation.append(sentence2)                     

                    else:
                        cols[0] = 'my' # language code
                        cols[6] = my_dict.get(sentence1, sentence1)
                        cols[7] = my_dict.get(sentence2, sentence2)
                        cols[-1] = cols[-1].strip()
                        out_cols = cols

                    # Clean characters that will corrput the TSV format
                    out_cols_clean = []
                    for col in out_cols:
                        col = col.replace('\t', '')
                        col = col.replace('"', '')
                        out_cols_clean.append(col)

                    outfile.write('\t'.join(out_cols_clean) + '\n')

            outfile.close()
            print(len(no_translation) , 'sentences not translated.')
            print ('\n'.join(set(no_translation)))


    # TODO: Add a new column to the parallel corpus


if __name__ == '__main__':

    # Build output files
    mydict, stats = build_dict()
    print(stats)
    write_dataset(mydict)
    write_source_sentences(mydict)
        
           

        
            