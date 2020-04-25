#!/bin/bash

rm processed*
# rm -i processed*
# if [[ $answer =~ ^processed*  ]]; then
# ...
# fi

cnt=0
for i in `ls *.txt`; do
    ((cnt += 1))
    echo Processsing text: $i
    python3 textMining-preprocess.py $i 2> /dev/null
done
echo $cnt texts has been processed
