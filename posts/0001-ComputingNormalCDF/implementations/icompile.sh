#! /usr/bin/env zsh

echo "Compiling C++ implementations ..."
clang++ -std=c++2a implementations.cpp -O3 -o impcpp