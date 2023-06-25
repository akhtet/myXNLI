
import sys, random

USAGE = """
python script/sample-devset.py sequence_file sample_size
"""

dev_sets = {
    'en1': {
        'input': 'output/myxnli.dev.tsv',
        'output': 'output/sample1.en.myxnli.dev.tsv',
        'label_index': 0,
        'sentence1_index': 1,
        'sentence2_index': 2     
    },
    'en2': {
        'input': 'output/myxnli.dev.tsv',
        'output': 'output/sample2.en.myxnli.dev.tsv',
        'label_index': 0,
        'sentence1_index': 1,
        'sentence2_index': 2,        
    },
    'my1': {
        'input': 'output/myxnli.dev.tsv',
        'output': 'output/sample1.my.myxnli.dev.tsv',
        'label_index': 0,
        'sentence1_index': 3,
        'sentence2_index': 4             
    },    
    'my2': {
        'input': 'output/myxnli.dev.tsv',
        'output': 'output/sample2.my.myxnli.dev.tsv',
        'label_index': 0, 
        'sentence1_index': 3,
        'sentence2_index': 4     
    }
}

if __name__ == '__main__':

    sample_file =sys.argv[1]
    sample_seqs = [ int(line.strip()) for line in open(sample_file).readlines()]
    
    sample_size = int(sys.argv[2])

    assert(len(sample_seqs)) > sample_size
    print(sample_seqs[0:10])

    batch = 0
    for lang in ['en1', 'en2', 'my1', 'my2']:
        input_filename = dev_sets[lang]['input']
        output_filename = dev_sets[lang]['output']

        with open(input_filename, encoding='utf-8') as infile:
    
            outfile = open(output_filename, 'wt', encoding='utf-8')          
            outfile.write('\t'.join(['seq', 'label', 'sentence1', 'sentence2','new_label', 'comments', '\n']))  # Write header

            lines = infile.readlines()
  
            for seq in sorted(sample_seqs[batch*sample_size: (batch*sample_size)+sample_size]):
                cols = lines[seq].strip().split('\t')
                new_cols = [
                    str(seq),
                    cols[dev_sets[lang]['label_index']],
                    cols[dev_sets[lang]['sentence1_index']],
                    cols[dev_sets[lang]['sentence2_index']],
                    ''
                    '\n'
                ]

                outfile.write('\t'.join(new_cols))
                print(seq)
            
            outfile.close()
        batch += 1
   