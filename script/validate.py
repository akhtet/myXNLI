
import csv, sys, os, re, yaml

def analyze_file(file_path, trans_dict={}):
    """
    Finds issues with a single translation file:
    - Missed sequences
    - Remaining Review Tags
    - Spelling errors / Find and replace
    - Tabs, doublequotes in lines

    The output dict "blocks" format is
    file_name: string
        sequence number: integer
            source: string
            target: string
            rating: integer     
            review: boolean
            comments: list[string]
            errors: list[string]

    The output list "orphans" contain lines that does not belong to any block
    """

    def is_seq_num(line):
        return re.match('\d+$', line)

    def is_comment(line):
        return line.startswith('#')

    def is_English(line):
        maxchar = max(line)
        return maxchar < u'\u1000'  
        # NOTE: This only check for non-Burmese content, so not necessarily ASCII

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

    def is_rating(line):
        return re.match('^#?\s*[1-5]/5$', line.strip())
    
    def get_rating(line):
        bits = line.strip('#').strip().split('/')
        return int(bits[0])

    def is_tagged_review(comments):
        for line in comments:
            if re.match('^#.*REVIEW.*$', line, re.IGNORECASE):
                return True
        return False
   
    blocks = {}
    orphans = {}

    state = 0   # Init or blank line
    line_num = 0

    with open(file_path, encoding='utf-8') as infile:
        for line in infile.readlines():
            line_num += 1
            line = line.strip()
            
            if state == 0:  # Ready for sequence number
                if is_seq_num(line):     # Found the beginning of next block
           
                    seq_num = int(line)
                    blocks[seq_num] = {
                        'source': '',
                        'target': '',
                        'rating': 0,
                        'review': True,
                        'comments': [],
                        'errors': []
                    }                
                    state = 1
                elif is_comment(line) or is_blank(line):
                    continue
                else:
                    orphans[line_num] = line

            elif state == 1:    # Ready for source sentence
                if is_English(line.strip()):
                    blocks[seq_num]['source'] = line
                else:
                    blocks[seq_num]['errors'].append('Unrecognized source sentence')
                state = 2
            
            elif state == 2:    # Ready for target sentence
                if is_Burmese(line.strip()):
                    blocks[seq_num]['target'] = line
                    if is_invalid(line):
                        blocks[seq_num]['errors'].append('Invalid characters found in translation')

                    # Check against existing dictionary entries for consistency  
                    for word in blocks[seq_num]['source'].lower().split():
                        if word in trans_dict:
                            if not trans_dict.get(word) in line:
                                blocks[seq_num]['errors'].append('Inconsistent translation for "%s"' % (word))

                elif line == '<MYANMAR UNICODE TRANSLATION HERE>':
                    blocks[seq_num]['errors'].append('Missing Translation')                                   
                else:
                    blocks[seq_num]['errors'].append('Missing Target Sentence')
                state = 3

            elif state == 3:    # Ready for rating, comment or a blank line
            
                if is_rating(line):
                    blocks[seq_num]['rating'] = get_rating(line)
                
                elif is_comment(line):
                    blocks[seq_num]['comments'].append(line)

                elif is_blank(line):
                    
                    if blocks[seq_num]['rating'] == 0:
                        blocks[seq_num]['errors'].append('Missing Rating')

                    if len(blocks[seq_num]['errors']) == 0 and not is_tagged_review(blocks[seq_num]['comments']):
                        blocks[seq_num]['review'] = False

                    state = 0
                else:
                    orphans[line_num] = line

        else:   # Check the last sentence in a file, as it may not encounter a blank line
            if state == 3:
                if blocks[seq_num]['rating'] == 0:
                    blocks[seq_num]['errors'].append('Missing Rating')

                if len(blocks[seq_num]['errors']) == 0 and not is_tagged_review(blocks[seq_num]['comments']):
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


if __name__ == '__main__':

    if len(sys.argv) > 1:
        for fpath in sys.argv[1:]:
            blocks, orphans = analyze_file(fpath)
            summarize_errors(blocks, orphans)