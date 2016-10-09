#!/bin/bash
#
# Usage:    [... dirs] run [... command]
# Exmaple:  ./fordirs.sh dir1 dir2 dirs* run ls -a

if [ -z "$2" ]
    then
        echo "Usage is ./runDirs"
        exit 1
fi

directories=()
run=()
found_run=false

for var in "$@"
do
    if [ "$found_run" = true ]
    then
        run+=("$var")
    else
        if [ "$var" = "run" ]
        then
            found_run=true
        else
            directories+=("$var")
        fi
    fi
done

if [ -z $run ]
then
    echo "Need to supply run command"
    exit 1
fi

for d in "${directories[@]}"
do
    test -d "$d" || continue
    # Do something with $dir...
    echo "---> $d"
    cd "$d"
    "${run[@]}"
    cd ..
done
