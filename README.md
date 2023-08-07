# myXNLI
Myanmar extension to XNLI Corpus

This project will add a Myanmar (Burmese) Corpus to the Cross Lingual NLI Corpus.
The original XNLI Corpus and paper can be found at https://github.com/facebookresearch/XNLI

## Acknowledgement
Contributed by the following volunteers

### Initial Translation
* Aung Kyaw Htet
* Aye Mya Hlaing
* Aye Nyein Mon
* Ei Myat Myat Noe
* Haymar Soe Naing
* Hnin Nandar Zaw
* Hsu Myat Mo
* Myint Wai
* Yimon Shwe Sin
* Win Pa Pa
* Win LL Phyu
* Yadanar
* Zaw Mee

### Translation Revision
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
