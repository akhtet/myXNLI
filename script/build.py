"""
Run this script from the main directory.
"""

import csv, sys, os, re, yaml

dev_file = 'xnli-original/xnli.dev.tsv'
test_file = 'xnli-original/xnli.test.tsv'
parallel_file = 'xnli-origin/xnli.15way.orig.tsv'

trans_dir = 'translation'
my_dev_file = 'output/myxnli.dev.tsv'
my_test_file = 'output/myxnli.test.tsv'

keyword_file = 'translation/keywords.csv'
en_sentence_file = 'translation/english.txt'

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


def load_keywords():
    keywords = {}
    with open(keyword_file, encoding='utf-8') as infile:
        reader = csv.reader(infile)
        keywords = {rows[0].lower():rows[1] for rows in reader} # TODO: allow multiple values
    return keywords


def analyze_file(fname):
    """
    Finds issues with the translation file:
    - Missed sequences
    - Review Tags
    - Spelling errors / Find and replace
    - Tabs, doublequotes in lines

    The output dict format is
    file_name: string
        sequence number: integer
            source: string
            target: string
            review: boolean            
            comments: list[string]
            errors: list[string]
    """

    def is_seq_num(line):
        return re.match('\d+$', line)

    def is_comment(line):
        return line.startswith('#')

    def is_English(line):
        maxchar = max(line)
        return maxchar < u'\u1000'  
        # NOTE: This only check for non-Burmese line, so not necessarily ASCII
        # return re.match('[A-Za-z0-9]+', line.split()[0])

    def is_Burmese(line):
        maxchar = max(line)
        return u'\u1000' <= maxchar <= u'\u200c' # u'\u109f'

    def is_blank(line):
        return len(line) == 0

    def is_invalid(line):
        for token in line.split():
            if '"' in token:
                return True
            if '\t' in token:
                return True
        return False

    def is_review(comments):
        for line in comments:
            if re.match('^#.*REVIEW.*$', line, re.IGNORECASE):
                return True
        return False

    blocks = {}
    orphans = {}

    keywords = load_keywords()

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
                if is_Burmese(line):
                    blocks[seq_num]['target'] = line
                    if is_invalid(line):
                        blocks[seq_num]['errors'].append('Invalid characters found in translation')

                    # Check against existing dictionary entries for consistency
                    
                    for word in blocks[seq_num]['source'].lower().split():
                        if word in keywords:
                            if not keywords.get(word) in line:
                                blocks[seq_num]['errors'].append('Inconsistent translation for "%s"' % (word))

                elif line == '<MYANMAR UNICODE TRANSLATION HERE>':
                    blocks[seq_num]['errors'].append('Missing Translation')                                   
                else:
                    blocks[seq_num]['errors'].append('Missing Target Sentence')

                state = 3
            else:
                if is_comment(line):
                    blocks[seq_num]['comments'].append(line)

                elif is_blank(line):
                    if len(blocks[seq_num]['errors']) == 0 and not is_review(blocks[seq_num]['comments']):
                        blocks[seq_num]['review'] = False
                    state = 0
                else:
                    orphans[line_num] = line
        else:   # Check the last sentence in a file
            if state == 3:
                if len(blocks[seq_num]['errors']) == 0 and not is_review(blocks[seq_num]['comments']):
                        blocks[seq_num]['review'] = False

    return blocks, orphans


def summarize_errors(blocks, orphans):

    summary = {
        'blocks' : 0,
        'reviews' : 0,
        'orphans' : []
    }

    errors = []     # This will become additional keys in summary

    seqs = blocks.keys()

    for b in range(min(seqs), max(seqs)+1):
    
        if not b in blocks:
            print('Missing block:', b)
            errors.append('Missing Block')
            continue

        summary['blocks'] += 1
        display=False

        if blocks[b]['review']:
            summary['reviews'] += 1
            display = True

        if len(blocks[b]['errors']) > 0:
            errors += blocks[b]['errors']
            display = True

        if display:
            print(b)
            #print(yaml.dump(blocks[b], encoding='utf-8'))
            print(blocks[b])
            print('')

    for o in orphans:
        summary['orphans'].append(o)

    for e in errors:
        summary[e] = 1 + summary.get(e, 0)

    print('SUMMARY')
    print(yaml.dump(summary))


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
            print ('Writing ', outfn)
            outfile = open(outfn, 'wt', encoding='utf-8')

            if OUTPUT_FORMAT == 'BASIC':
                outfile.write('\t'.join(['label', 'sentence1_en', 'sentence2_en', 'sentence1_my', 'sentence2_my']) + '\n')
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
                                sentence1,
                                sentence2,
                                my_dict.get(sentence1, sentence1),
                                my_dict.get(sentence2, sentence2)
                                ]

                        # Clean characters that will corrput the TSV format
                        out_cols_clean = []
                        for col in out_cols:
                            col = col.replace('\t', '')
                            col = col.replace('"', '')
                            out_cols_clean.append(col)

                        outfile.write('\t'.join(out_cols_clean) + '\n')

                    else:
                        cols[0] = 'my' # language code
                        cols[6] = my_dict.get(sentence1, sentence1)
                        cols[7] = my_dict.get(sentence2, sentence2)
                        outfile.write('\t'.join(cols))

            outfile.close()

    # TODO: Add a new column to the parallel corpus


if __name__ == '__main__':

    if len(sys.argv) == 1:
        mydict, stats = build_dict()
        print(stats)
        write_dataset(mydict)
        write_source_sentences(mydict)
    else:

        for fname in sys.argv[1:]:
            blocks, orphans = analyze_file(fname)
            summarize_errors(blocks, orphans)
           

        
            