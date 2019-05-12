#!/bin/bash
tests=("../tests/in/9.in" "../tests/in/10.in")

for test in "${tests[@]}"
do
    echo "$test"
    time python3 src/main.py < $test > o.txt
    echo ""
done