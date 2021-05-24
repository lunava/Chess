#!/bin/bash
dir=$1
for file in "$(find $dir -name *.py)"
do 
    if [[ "$file" != "$dir/__init__.py" ]];then
        printf '%s\n ' "$file" 
        python3 -m unittest $file
    fi
done