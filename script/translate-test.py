from google.cloud import translate_v2 as translate

import sys

#export GOOGLE_APPLICATION_CREDENTIALS="<path>/<credential.json>"

test_sets = {
    'my': {
        'input': 'output/myxnli.test.tsv',
        'output': 'output/myxnli.trans.test.raw.tsv',
        'lang_index': -1,
        'label_index': 0,
        'sentence1_index': 3,
        'sentence2_index': 4    
    },
    'sw': {
        'input': 'xnli-original/xnli.test.tsv',
        'output': 'output/swxnli.trans.test.raw.tsv',
        'lang_index': 0,
        'label_index': 1,
        'sentence1_index': 6,
        'sentence2_index': 7,      
    },
    'ur': {
        'input': 'xnli-original/xnli.test.tsv',
        'output': 'output/urxnli.trans.test.raw.tsv',
        'lang_index': 0,
        'label_index': 1,
        'sentence1_index': 6,
        'sentence2_index': 7,      
    }
}


def translate_all(sentences, target_language='en'):
    """Translates text into the target language.
    Keeps a memory of previous sentences translated.
    """
    global translation_mem

    to_translate = [ source for source in sentences if source not in translation_mem ]

    if len(to_translate) > 0:
        results = translate_client.translate(to_translate, target_language=target_language)
        for result in results:
           translation_mem[result['input']] = result['translatedText'] 
      
    return [translation_mem[source] for source in sentences]


def postprocess_line(line):
    """
    Cleans certain tokens in the output file that creates parsing issues
    """
    out_cols_clean = []

    for col in line.split('\t'):
        if col.lower() == 'n/a': 
            col = 'not applicable'
        else:
            col = col.replace('&#39;', "'")
            col = col.replace('&quot;', "'")
        out_cols_clean.append(col)
   
    return '\t'.join(out_cols_clean)


if __name__ == '__main__':
   
    lang = sys.argv[1]
    input_filename = test_sets[lang]['input']
    output_filename = test_sets[lang]['output']
    lang_index = test_sets[lang]['lang_index']
    label_index = test_sets[lang]['label_index']
    sentence1_index = test_sets[lang]['sentence1_index']
    sentence2_index = test_sets[lang]['sentence2_index']

    if sys.argv[-1] == 'post':
         
         with open(output_filename, encoding='utf-8') as infile:
            with open(output_filename + '.post', 'wt', encoding='utf-8') as outfile:
                for line in infile.readlines():
                    outfile.write(postprocess_line(line.strip()) + '\n')
                outfile.close()

    else:

        translation_mem = {}
        translate_client = translate.Client()

        skip = 0
        counter = 0

        with open(input_filename, encoding='utf-8') as infile:
            
            if sys.argv[-1] == 'resume':
                outfile = open(output_filename, 'rt', encoding='utf-8')
                skip = len(outfile.readlines()) - 1
                outfile.close()
                outfile = open(output_filename, 'at', encoding='utf-8')
            else:
                outfile = open(output_filename, 'wt', encoding='utf-8')
                outfile.write('\t'.join(['label', 'sentence1_en', 'sentence2_en', 'sentence1_' + lang, 'sentence2_' + lang]) + '\n')
            
            infile.readline()  # Skip header
        
            for line in infile.readlines():

                cols = line.split('\t')

                if lang_index >= 0 and cols[lang_index] != lang:
                    continue

                if skip > 0:
                    skip -= 1
                    counter += 1
                    if counter % 500 == 0 or skip == 0:
                        print ('Skipped: %d, Remaining: %d ' % (counter, skip))
                    continue

                gold_label = cols[label_index]
                sentence1 = cols[sentence1_index]
                sentence2 = cols[sentence2_index]
                sentence1_en, sentence2_en = translate_all([sentence1, sentence2])

                out_cols = [
                    gold_label,
                    sentence1_en,
                    sentence2_en,
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
                if counter % 1000 == 0:
                    print ('Line %d, Translations: %d' % (counter, len(translation_mem)))
            outfile.close()