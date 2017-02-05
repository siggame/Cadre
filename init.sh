#!/bin/bash
# This script will initialize all the Cadre subrepos for you
# It simply initializes each subrepository, then checkouts the
# master branch for each subrepo

git submodule update --init --recursive
exec ./fordirs.sh Cerveau/ Creer/ Viseur/ Joueur.* run git checkout master
exec ./fordirs.sh Cerveau/ Creer/ Viseur/ Joueur.* run git pull
