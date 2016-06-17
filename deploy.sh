#!/usr/bin/env bash
if [ -z "$1" ]
  then
    echo "No commit message supplied"
    exit 1
fi
python build.py
git add --all :/
git commit -m "$1"
git push origin master
