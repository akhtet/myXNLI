
data_sets = {
    'sw_test': {
        'input': 'xnli-original/xnli.test.tsv',
        'output': 'output/sw/sw.test.tsv'  
    },
    'ur_test': {
        'input': 'xnli-original/xnli.test.tsv',
        'output': 'output/ur/ur.test.tsv'   
    },
    'sw_dev': {
        'input': 'xnli-original/xnli.dev.tsv',
        'output': 'output/sw/sw.dev.tsv'  
    },
    'ur_dev': {
        'input': 'xnli-original/xnli.dev.tsv',
        'output': 'output/ur/ur.dev.tsv'   
    }
}

lang_index = 0
label_index = 1
genre_index = 10
sentence1_index = 6
sentence2_index = 7

if __name__ == '__main__':
   
    for dataset in data_sets.keys():

        input_filename = data_sets[dataset]['input']
        output_filename = data_sets[dataset]['output']
        print (output_filename)

        lang = dataset.split('_')[0]
        counter = 0

        with open(input_filename, encoding='utf-8') as infile:
            
            outfile = open(output_filename, 'wt', encoding='utf-8')
            outfile.write('\t'.join(['genre', 'label', 'sentence1_' + lang, 'sentence2_' + lang]) + '\n')
            
            infile.readline()  # Skip header
        
            for line in infile.readlines():

                cols = line.strip().split('\t')

                if cols[lang_index] != lang:
                    continue

                gold_label = cols[label_index]
                genre = cols[genre_index]
                sentence1 = cols[sentence1_index]
                sentence2 = cols[sentence2_index]
             
                out_cols = [
                    genre,
                    gold_label,
                    sentence1,
                    sentence2
                ]

                # Clean characters that will corrput the TSV format
                out_cols_clean = []
                for col in out_cols:
                    col = col.replace('\t', '')
                    col = col.replace('"', '')
                    out_cols_clean.append(col)

                outfile.write('\t'.join(out_cols_clean) + '\n')

                counter += 1           
                if counter % 500 == 0:
                    print ('Line %d' % (counter))

            outfile.close()