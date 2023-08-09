# Myanmar Translation QA

##  FILE FORMAT

Translation files assigned to you for QA can be found in the folder under your name or initials.

There are 100 sentence blocks in each file. Each block has the following format.
- First line for sequence number, 
- Second line for English source sentence
- Third line for Myanmar translation -- You can overwrite it with your correction.
- Fourth line for the rating of final translation between (1-5) -- This is for you to add.
- Fifth line is a blank line for sepearating between the blocks

Here is an example block.
```
114
We were watching something on TV.
ကျွန်တော်တို့ တီဗီမှာ တခုခု ကြည့်နေခဲ့သည်။
# 5/5
# The above number is the translation rating, but this line is an optional comment 
```



##  QA PROCEDURE

1. Do not add or remove any lines to the files (except for optional comments/notes that start with a `#`)
2. Comments are optional translation notes for anything you want to discuss with the wider group.
     Any number of lines for comments (notes) can be added to the block by starting with a Hash `#`.    
3. Do not correct the English sentence under any circumstances.
4. Correct the Myanmar Translation if it is mistranslated, or can be improved.
     To correct, just overwrite the Myanmar sentence. DO NOT keep older versions of Myanmar Translation.
5. Give a translation quality rating to the final version of the Myanmar sentence.

Translation rating is out of 5
     
    5/5 = Translation is perfect
    4/5 = Translation is somewhat unnatural, but the overall meaning is correct
    3/5 = Translation is partially correct, but missing some details
    2/5 = Translation is wrong or misleading
    1/5 = Translation is incomprehensible
 
## GENERAL TRANSLATION GUIDANCE

1. Don't miss any information in translation
2. Don't add unnecessary information
3. Take care to minimise spelling mistakes in Myanmar sentence
4. Use the spoken or written style of Myanmar, depending on the English sentence (e.g. သည်၊ မည်၊ vs. တယ်၊ မယ်)
5. If possible, use the Myanmar terms that directly align to English (i.e. avoid idiomatic translation)

## HOW TO HANDLE SPECIAL CASES

1. English Terms

    If there is no commonly used Burmese word for an English term, just use the English words back in Myanmar Translation. However for uncommon English words, it is OK to use them as English in the Translation.
    
    For example, it is OK to translate "England" as "အင်္ဂလန်" becuase the word exists in Burmese Literature.
    But names like "James Whitcomb Riley, Eugene V. Debs and Madam C.J" should be just used as-is in English in the translation.
    
    The usage of Myanmar or English word for a name/term should be consistent across all files. For example, do no use "အင်္ဂလန်" in once place and then use "England" in another place.

2. Mistranslations due to cultural difference

    For example, the term "Indians" can refer to Native Indians, rather than အိန္ဒိယလူမျိုး that is closer to Burmese culture. If you are not sure, just reuse the English word "Indians"

3. Present Tense / Past Tense correctness 

    Look out for mistakes in translating tenses. e.g. Go/Went/Gone = သွားသည်/သွားခဲ့သည်/သွားပြီးပြီ 


## EXAMPLES

You can see some examples of QA output below. 
Don't worry if it is too hard to get the perfect translation. Just try to improve it. 
It is good enough if your FINAL translations can get to (4/5) rating.

###  Example 1: Simplification

Before QA
```
9918
Japan and Sweden are members of the Auld Alliance.
ဂျပန်နှင့် ဆွီဒင်တို့သည် နိုင်ငံအချင်းချင်း တဦးနှင့်တဦး ကူညီထောက်ပံ့ရန်နှင့် ကာကွယ်ပေးရန် သဘောတူညီချက် အော့ဒ်ထ်၏ အဖွဲ့ဝင်များဖြစ်ကြသည်။
```

After QA
```
9918
Japan and Sweden are members of the Auld Alliance.
ဂျပန်နှင့် ဆွီဒင်တို့သည် Auld မဟာမိတ် အဖွဲ့ဝင်များဖြစ်ကြသည်။
# 5/5
```

### Example 2: Adaptation

Before QA
```
9940
Six more scotches on the rocks will do just fine.
ကျောက်တုံးကြီးများပေါ်မှ နောက်ထပ် စကော့တလန်ဝီစကီ ခြောက်ခွက် သည် ကောင်းကောင်းလုပ်ဆောင်မည်။
```

After QA
```
9940
Six more scotches on the rocks will do just fine.
နောက်ထပ် ရေမရောသော စကော့တလန်ဝီစကီ ခြောက်ခွက် အတွက် အဆင်ပြေသေးသည်။
# 4/5
```


### Example 3: Direct reuse of English terms

Before QA
```
9989
Fiesty began as fisten.
စိတ်ပြင်းပြခြင်းသည် လက်သီးဆုပ် အဖြစ် စတင်သည်။
```

After QA
```
9989
Fiesty began as fisten.
Fiesty သည် fisten အဖြစ် စတင်ခဲ့သည်။
# 5/5
```
### Example 4: Correcting Semantics 

Before QA
```
9010
The AFI makes choices that can be considered arbitrary.
အေအက်ဖ်အိုင် သည် တစ်ဖက်သတ် ယူဆနိုင်သော ရွေးချယ်မှုများ ပြုလုပ်သည်။
```

After QA
```
9010
The AFI makes choices that can be considered arbitrary.
AFI သည်  ကြိုးကြောင်းမဆီလျော်သော ရွေးချယ်မှုများ ပြုလုပ်နိုင်သည်ဟုယူဆနိုင်သည်။
# 4/5
```

### Example 5: Improving Semantics 

Before QA
```
9074
The insanity only lasted for a day.
ရူးသွပ်မှုက တစ်ရက်သာ ကြာမြင့်တယ်။
```

After QA
```
9074
The insanity only lasted for a day.
ဒီရူးသွပ်မှုက တစ်ရက်သာ ကြာမြင့်ခဲ့တယ်။
# 4/5
```

## HOW MUCH TIME SHOULD YOU TAKE

Our target is to complete 1 file per week per contributor.

Each block should take you 1-2 minutes. Do not spend more than 5 minutes on each block. 

Each file has 100 blocks and it can take up to two hours, depending on the contents in individual files.

While everyone's schedule is different, you may find that it is easier to do 20 blocks per day, rather than doing it all in one go.

## TEAM CHAT

Still have questions or suggestions? 

Connect to our team chat at https://discord.gg/wj4yCVU6pU
