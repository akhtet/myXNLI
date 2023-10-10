#-*- coding:utf-8 -*- 

##
## syllable breaking tool for Myanmar language
## usage: sylbreak3.py -i input-file
## e.g. usage1: python ./sylbreak3.py -i ../data/my-input.txt
##      usage2: ./sylbreak3.py -i ../data/my-input.txt -o out.txt -s " "
## 
## Date: 21 July 2016
## Written by Ye Kyaw Thu, Visiting Researcher, Waseda University
## HP:https://sites.google.com/site/yekyawthunlp/
##
## last updated: 29 Sep 2021 
## Add support for python3 by sengkyaut
##
## Reference of Myanmar Unicode: http://unicode.org/charts/PDF/U1000.pdf
##
## LICENSE: https://github.com/ye-kyaw-thu/sylbreak/blob/master/LICENSE

import re

myConsonant = r"က-အ"
enChar = r"a-zA-Z0-9"
otherChar = r"ဣဤဥဦဧဩဪဿ၌၍၏၀-၉၊။!-/:-@[-`{-~\s"
ssSymbol = r'္'
aThat = r'်'

#Regular expression pattern for Myanmar syllable breaking
#*** a consonant not after a subscript symbol AND a consonant is not followed by a-That character or a subscript symbol

BreakPattern = re.compile(r"((?<!" + ssSymbol + r")["+ myConsonant + r"](?![" + aThat + ssSymbol + r"])" + r"|[" + enChar + otherChar + r"])")

def sylbreak(line):
       line = re.sub(r"\s+","", line)
       line = BreakPattern.sub(r" " + r"\1", line)
       return line
