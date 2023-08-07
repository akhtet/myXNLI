# myXNLI
Myanmar extension to XNLI Corpus

This project will add a Myanmar (Burmese) Corpus to the Cross Lingual NLI Corpus.
The original XNLI Corpus and paper can be found at https://github.com/facebookresearch/XNLI

## Acknowledgement
Contributed by the following volunteers

### Dataset Translation
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

### Dataset Revision
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

## Myanmar Translation Instructions

Under `translation` folder, there are 100 files, each containing 100 blocks. Each block has a block number, an English sentence and a placeholder for Myanmar Translation.

For example:
```
114
We were watching something on TV.
<MYANMAR UNICODE TRANSLATION HERE>
```

As a translator, you can pick any file and add missing translations at the tag <MYANMAR UNICODE TRANSLATION HERE>, and keep other sentences intact. Please use only Myanmar Unicode font in your translations. You are also requested to separate Buremse phrases by spaces where it makes sense, and use ပုဒ်မ `။` as a sentence terminator.

After translation:
```
114
We were watching something on TV.
ကျွန်တော်တို့ တီဗီမှာ တခုခု ကြည့်နေခဲ့သည်။
```

If you have been added to the project, you are welcome to directly update the translation files.
If you are an external contributor, we welcome pull requests.

### Comments 
 
Use # to insert a comment line at the bottom of the each block.
Any number of comment lines can be used as long as they are after the sequence number line.
 
```
114
We were watching something on TV.
ကျွန်တော်တို့ တီဗီမှာ တခုခု ကြည့်နေခဲ့သည်။
# This is a comment
```

 
### Tags
 
Any translation that is difficult or ambiguous should be reviewed regularly among the translation.
You can leave a comment with the tag # REVIEW to mark any translations that needs to be reviewed.
 
```
114
We were watching something on TV.
ကျွန်တော်တို့ တီဗီမှာ တခုခု ကြည့်နေခဲ့သည်။
# REVIEW
# This is a comment explaining details about the problem.
```
