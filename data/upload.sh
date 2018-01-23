#!/bin/bash
FILES=$PWD
for f in *; do
  echo "Processing $f file..."
  # take action on each file. $f store current file name
  mongoimport --db test --collection Jan22_tweets_untagged --file $f
done
