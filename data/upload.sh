#!/bin/bash
FILES=$PWD
for f in *; do
  echo "Processing $f file..."
  # take action on each file. $f store current file name
  mongoimport --db test --collection tweets_collection --file $f
done
