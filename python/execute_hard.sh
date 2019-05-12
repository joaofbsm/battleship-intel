#!/bin/bash
tests=("../tests/in/9.in" "../tests/in/10.in")

for test in "${tests[@]}"
do
    echo "$test"
    time python src/main.py < $test > ../results/pdf1.out
    echo ""
done