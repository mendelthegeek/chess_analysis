#!/bin/bash

file_name=${1?Please enter a pgn file to analize}

clear

rm test.log

echo -e "\nTime: $(date)" > test.log

python analyze-pgn.py $file_name.pgn 1>> test.log 2> test.err

echo LOG:
cat test.log

echo ERROR FILE SIZE:
echo $(stat -c%s "test.err")

while true; do
    read -p "Do you wish to append this log? (y/n)" yn
    case $yn in
        [Yy]* ) cat test.log >> tests.log; break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done
