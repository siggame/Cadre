#!/bin/bash

sed 's/git\@github.com\:/https:\/\/github.com\//g' .gitmodules > temp.txt
rm .gitmodules
mv temp.txt .gitmodules
