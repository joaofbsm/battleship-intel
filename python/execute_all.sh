#!/bin/bash
tests=("../tests/in/1.in" "../tests/in/2.in" "../tests/in/3.in" "../tests/in/4.in" "../tests/in/5.in" "../tests/in/6.in" "../tests/in/7.in" "../tests/in/8.in" "../tests/in/9.in" "../tests/in/10.in" "../tests/in/pdf1.in" "../tests/in/pdf2.in")

for test in "${tests[@]}"
do
    echo "$test"
    time python src/main.py -i $test -o ../results/pdf1.out
    echo ""
done