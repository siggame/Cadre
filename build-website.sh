#!/bin/bash

echo ">> Building Cadre website <<"

cd Website
# build the static site
npm install
npm run build
# file to tell GitHub pages not to try to run jekyll stuff (can break urls)
touch output/.nojekyll

echo ">> Wesbite built <<"
