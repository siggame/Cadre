#!/bin/bash
# This script will initialize all the Cadre subrepos for you
# It simply initializes each subrepository, then checkouts the
# master branch for each subrepo

echo ">> Initializing all submodules with git <<"
git submodule update --init --recursive

submodules=($(git config --file .gitmodules --get-regexp path | awk '{ print $2 }'))
for submodule in "${submodules[@]}"; do
    echo "--> ${submodule} <---"
    cd ${submodule}
    git checkout master
    git pull
    cd ..
done

echo ">> Cadre repos initialized, exiting <<"
