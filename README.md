# myXNLI
Myanmar XNLI - Myanmar extension to the XNLI Corpus

The myXNLI dataset extends the XNLI Corpus with Myanmar (Burmese) language.
The original XNLI Corpus and paper can be found at https://github.com/facebookresearch/XNLI

For myXNLI, we translated all 7,500 sentence pairs from XNLI English dev/test sets into Myanmar. The labels from English dev/test sets are also reused for the Myanmar datasets.

The dataset also includes the NLI training data in Myanmar which is created by machine-translating the MultiNLI training data from English into Myanmar. Similar to XNLI, we also reuse the existing labels for English training data for the Myanmar version.

## Downloads
* Myanmar NLI Test Dataset - 5010 records [(tsv)](./output/my/my.genre.test.tsv)
* Myanmar NLI Validation Dataset - 1490 records [(tsv)](./output/my/my.genre.dev.tsv)
* Myannmar NLI Training Data - 392,702 records [(tsv.gz)](./output/my/my.genre.train.tsv.gz)
* Parallel Corpus 16 Languages [(tsv)](./output/my/myxnli.16way.tsv)

## NLI Format

First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell

## Myanmar Translation Entry Format

Under `translation` folder, there are 100 files, each containing 100 blocks. Each block has a block number, an English sentence and a placeholder for Myanmar Translation. An example entry in a translation file is describe below.

```
114
We were watching something on TV.
ကျွန်တော်တို့ တီဗီမှာ တခုခု ကြည့်နေခဲ့သည်။
# REVIEW
# This is a comment explaining details about the problem.
```


The first line makes a reference to the line number of the English sentence in the XNLI corpus. 

The second line contains the actual English sentence to be translated.

The third line is reserved for Myanmar translation of the English sentence.

Additional and optional lines for human translator notes are also allowed with a hash prefix (#). This is useful for flagging translations that require review or documenting any observations made during translation.

Lastly, each entry in the file is separated by a blank
line followed by another entry.

## Acknowledgements
This dataset is contributed by the following volunteers.

### Phase 1 - Core Translation Team
* Aung Kyaw Htet
* Aye Mya Hlaing
* Hsu Myat Mo
* Win Pa Pa
* Yimon Shwe Sin

### Phase 1 - Extended Translation Team
* Aye Nyein Mon
* Ei Myat Myat Noe
* Haymar Soe Naing
* Hnin Nandar Zaw
* Myint Wai*
* Win LL* Phyu
* Yadanar
* Zaw Mee

### Phase 3 - Translation Revision
* Aung Kyaw Htet
* Edward Law
* Junie Soe
* Thar Htet
* Thein Aung Tan
* Thidar Nwe
* Thiha Kyaw Zaw
* Yair Pike
* Yi Sandi Soe
  
### Sample Relabeling
* Htet Cho
* Lin Thurein Tun
* Thein Than Phyo
* Zay Ye Htut

