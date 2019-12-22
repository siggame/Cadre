#!/bin/bash

for repo in Cerveau Viseur Joueur.cpp Joueur.cs Joueur.go Joueur.java Joueur.js Joueur.lua Joueur.py Joueur.ts
do
    cd $repo
    echo " -> adding MMAI-dev branch for $repo"
    git remote add mmai-dev git@github.com:siggame/$repo-MegaMinerAI-Dev.git
    git fetch --all
    cd ..
done

