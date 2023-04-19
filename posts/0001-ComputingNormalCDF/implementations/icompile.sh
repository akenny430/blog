#! /usr/bin/env bash

case $OSTYPE in 
    'darwin22.0') compiler='clang++' ;; #  macbook 
    'msys') compiler='g++' ;; # coofun 
esac 

echo "Compiling C++ implementations ..."
$compiler -std=c++20 -O3 -Wall implementations.cpp -o impcpp