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

# BASIC: 'label', 'sentence1', 'sentence2'
# STANDARD: 
OUTPUT_FORMAT = 'BASIC' 


def build_dict():
    """
    Build a dictionary between EN and MY sentences 
    Summarises issues within each translation file   
    """
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
                elif re.match('\d+', line):     # Found the beginning of next block
                    state = 1
                elif state == 1:                # Get English Source Sentence
                    en_source = line
                    state = 2
                elif state == 2:                # Get Burmese Source Sentence
                    if line != '<MYANMAR UNICODE TRANSLATION HERE>':
                        my_dict[en_source] = line
                        file_stats[fname] = file_stats.get(fname, 0) + 1
                    state = 0
    
    print ('%d entries loaded to the dictionary' % len(my_dict.keys()))
    return my_dict, file_stats


def analyze_file(fname):
    """
    Missed sequences
    Review Tags
    Spelling errors / Find and replace
    Tabs, doublequotes

    file_name: string
        sequence number: integer
            source: string
            target: string
            review: boolean            
            comments: list[string]
            errors: list[string]

    """

    def is_seq_num(line):
        return re.match('\d+', line)

    def is_comment(line):
        return line.startswith('#')

    def is_English(line):
        return re.match('[A-Za-z]+', line.split()[0])

    def is_Burmese(line):
        maxchar = max(line)
        return u'\u1000' <= maxchar <= u'\u200c' # u'\u109f'

    def is_blank(line):
        return len(line) == 0

    def is_review(comments):
        for line in comments:
            if re.match('^#.*REVIEW.*$', line, re.IGNORECASE):
                return True
        return False

    blocks = {}
    orphans = {}

    state = 0   # Init or blank line
    line_num = 0

    with open(os.path.join(trans_dir, fname), encoding='utf-8') as infile:
        for line in infile.readlines():
            line_num += 1
            line = line.strip()
            
            if state == 0:
                if is_seq_num(line):     # Found the beginning of next block
           
                    seq_num = int(line)
                    blocks[seq_num] = {
                        'source': '',
                        'target': '',
                        'review': True,
                        'comments': [],
                        'errors': []
                    }                
                    state = 1
                else:
                    orphans[line_num] = line

            elif state == 1:              # Start new block
                if is_English(line):
                    blocks[seq_num]['source'] = line
                else:
                    blocks[seq_num]['errors'].append('Missing Source Sentence')
                state = 2
            
            elif state == 2:
                if is_Burmese(line) or line == '<MYANMAR UNICODE TRANSLATION HERE>':
                    blocks[seq_num]['target'] = line                                         
                else:
                    blocks[seq_num]['errors'].append('Missing Target Sentence')
                    # print (line)
                    # print (max(line))
                    # print (hex(ord(max(line))))
                    # print (is_Burmese(line))
                state = 3
            else:
                if is_comment(line):
                    blocks[seq_num]['comments'].append(line)

                elif is_blank(line):
                    if len(blocks[seq_num]['source']) > 0 and len(blocks[seq_num]['source']) > 0 and not is_review(blocks[seq_num]['comments']):
                        blocks[seq_num]['review'] = False
                    state = 0
                else:
                    orphans[line_num] = line
        else:
            if state == 3:
                if len(blocks[seq_num]['source']) > 0 and len(blocks[seq_num]['source']) > 0 and not is_review(blocks[seq_num]['comments']):
                        blocks[seq_num]['review'] = False

    return blocks, orphans
    #print ('%d entries loaded to the dictionary' % len(my_dict.keys()))
    #return my_dict, file_stats


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
    """
    Takes the original XNLI Dataset files and creates corresponding Burmese Dataset files
    Writes output files which can then be imported as MyXNLI Dataset
    """
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

    if len(sys.argv) == 1:
    # print(get_review_list())
        mydict, stats = build_dict()
        print(stats)
        write_dataset(mydict)
    else:
        for fname in sys.argv[1:]:
            blocks, orphans = analyze_file(fname)
            # Print only the blocks marked for review            
            [ print(b, blocks[b]) for b in blocks if blocks[b]['review'] ]
            [ print(orphans[o]) for o in orphans ]

            seqs = blocks.keys()
            min_seq = min(seqs)
            for seq in range(min(seqs), max(seqs)):
                if not seq in seqs:
                    print(seq, ' missing')
            print(len(seqs))