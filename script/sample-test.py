
import sys, random

test_sets = {
    'my': {
        'input': 'output/myxnli.test.tsv',
        'output': 'output/sample.myxnli.test.tsv',
        'lang_index': -1,
        'label_index': 0,
        'sentence1_index': 3,
        'sentence2_index': 4,
        'sentence1_en_index': 1,
        'sentence2_en_index': 2     
    }
}

if __name__ == '__main__':

    sample_size = int(sys.argv[1])

    input_filename = test_sets['my']['input']
    output_filename = test_sets['my']['output']

    with open(input_filename, encoding='utf-8') as infile:
    
        outfile = open(output_filename, 'wt', encoding='utf-8')          
        outfile.write(infile.readline())  # Write header

        lines = infile.readlines()
        line_count = len(lines)

        sample_seqs = random.sample(range(line_count), sample_size)

        for seq in sorted(sample_seqs):
            outfile.write(lines[seq])
            print(seq)
            
        outfile.close()