#!/usr/bin/env bash
python build.py
echo "Enter commit message: "
read message
git add --all :/
git commit -m "$message"
git push origin master
