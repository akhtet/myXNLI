# !/bin/bash
# This script should be run from the myXNLI directory

for f in `ls ../myTxQA/*/*.txt`; do
    echo $f; 
    cp $f translation/;
    sed -i '1,50d' translation/$f;
done
