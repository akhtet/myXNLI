"""
Run this script from the main directory.
"""

import csv, sys, os, re

dev_file = 'xnli-original/xnli.dev.tsv'
test_file = 'xnli-original/xnli.test.tsv'
parallel_file = 'xnli-origin/xnli.15way.orig.tsv'

trans_dir = 'translation'
my_dev_file = 'output/myxnli.dev.tsv'
my_test_file = 'output/myxnli.test.tsv'

# Create DEV and TEST files from the Originals
OUTPUT_FORMAT = 'BASIC' # STANDARD


def build_dict():

    # Build a dictionary between EN and MY sentences    
    my_dict = {}
    file_stats = {}

    for fname in os.listdir(trans_dir):
        print ('Processing', fname)   
        state = 0

        with open(os.path.join(trans_dir, fname), encoding='utf-8') as infile:            
            for line in infile.readlines():
                line = line.strip()
                if line.startswith('#'):
                    state = 0
                elif re.match('\d+', line):
                    state = 1
                elif state == 1:
                    en_source = line
                    state = 2
                elif state == 2:
                    if line != '<MYANMAR UNICODE TRANSLATION HERE>':
                        my_dict[en_source] = line
                        file_stats[fname] = file_stats.get(fname, 0) + 1
                    state = 0
    
    print ('%d entries loaded to the dictionary' % len(my_dict.keys()))
    return my_dict, file_stats


def get_review_list(context_size=2):

    review_list = {}
    
    for fname in os.listdir(trans_dir):
        print ('Processing', fname)   

        state = 0   # Going through each line
        context = []
        max_context_size = context_size * 2 + 1

        with open(os.path.join(trans_dir, fname), encoding='utf-8') as infile:            
            for line in infile.readlines():
                line = line.strip()

                context.append(line)
                if len(context) > max_context_size:
                    context.pop(0)

                if re.match('^#.*REVIEW.*$', line):     # Found a review tag
                    state = 1
                    next_lines = context_size
                elif state == 1:    # Adding context for a recently found review tag
                    next_lines = next_lines - 1
                    if next_lines == 0:
                        review_list[fname] = review_list.get(fname,[])
                        review_list[fname].append(context)
                        state = 0
    
    return review_list


def write_dataset(my_dict):    

    for infn, outfn in [(dev_file, my_dev_file), (test_file, my_test_file)]:
        with open(infn, encoding='utf-8') as infile:

            # Write the header
            print ('Writing ', outfn)
            outfile = open(outfn, 'wt', encoding='utf-8')

            if OUTPUT_FORMAT == 'BASIC':
                outfile.write('\t'.join(['label', 'sentence1', 'sentence2']) + '\n')
            else:
                outfile.write(infile.readline())

            for line in infile.readlines():
                if line.startswith('en'):
                    cols = line.split('\t')

                    # Column 7 and 8 are the unparsed English sentences
                    sentence1 = cols[6]
                    sentence2 = cols[7]

                    if OUTPUT_FORMAT == 'BASIC':
                        out_cols = [
                                cols[1], # label
                                my_dict.get(sentence1, sentence1),
                                my_dict.get(sentence2, sentence2)
                                ]
                        outfile.write('\t'.join(out_cols) + '\n')

                    else:
                        cols[0] = 'my' # language code
                        cols[6] = my_dict.get(sentence1, sentence1)
                        cols[7] = my_dict.get(sentence2, sentence2)
                        outfile.write('\t'.join(cols))

            outfile.close()

    # TODO: Add a new column to the parallel corpus

if __name__ == '__main__':

    # print(get_review_list())
    mydict, stats = build_dict()
    print(stats)
    write_dataset(mydict)