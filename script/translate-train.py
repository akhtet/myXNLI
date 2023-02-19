import six
from google.cloud import translate_v2 as translate

import sys

#export GOOGLE_APPLICATION_CREDENTIALS="<path>/<credential.json>"

input_train_file = 'xnli-original/multinli_1.0_train.txt'
output_train_file = 'output/myxnli.train.tsv'

translation_mem = {}
translate_client = translate.Client()


def translate_to_my(text):
    """Translates text into the target language.
    Keeps a memory of previous sentences translated.
    """
    global translation_mem

    if text not in translation_mem:

        if isinstance(text, six.binary_type):
            text = text.decode("utf-8")

        result = translate_client.translate(text, target_language='my')
        translation_mem[text] = result['translatedText']

    return translation_mem[text]


def translate_all_to_my(sentences):
    """Translates text into the target language.
    Keeps a memory of previous sentences translated.
    """
    global translation_mem

    to_translate = [ source for source in sentences if source not in translation_mem ]

    if len(to_translate) > 0:
        results = translate_client.translate(to_translate, target_language='my')
        for result in results:
           translation_mem[result['input']] = result['translatedText'] 
      
    return [translation_mem[source] for source in sentences]


if __name__ == '__main__':
   
    skip = 0
    counter = 0

    with open(input_train_file, encoding='utf-8') as infile:
        
        if sys.argv[1] == 'resume':
            outfile = open(output_train_file, 'rt', encoding='utf-8')
            skip = len(outfile.readlines()) - 1
            outfile.close()
            outfile = open(output_train_file, 'at', encoding='utf-8')
        else:
            outfile = open(output_train_file, 'wt', encoding='utf-8')
            outfile.write('\t'.join(['label', 'sentence1_en', 'sentence2_en', 'sentence1_my', 'sentence2_my']) + '\n')
        
        infile.readline()  # Skip header
       
        for line in infile.readlines():
            if skip > 0:
                skip -= 1
                counter += 1
                if counter % 1000 == 0 or skip == 0:
                    print ('Skipped: %d, Remaining: %d ' % (counter, skip))
                continue

            cols = line.split('\t')
            
            # in MultiNLI source file, column 6 and 7 are the unparsed English sentences
            gold_label = cols[0]
            sentence1_en = cols[5]
            sentence2_en = cols[6]
            sentence1_my, sentence2_my = translate_all_to_my([sentence1_en, sentence2_en])

            out_cols = [
                gold_label,
                sentence1_en,
                sentence2_en,
                sentence1_my,
                sentence2_my
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