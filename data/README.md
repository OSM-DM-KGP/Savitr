* mongoimport --db test --collection tweets_collection --file tweets_collection.json

* Make sure you drop the collection first.
* Use upload.sh to upload data.
```
cd data/Tagged/
sh ../upload.sh
cd ../Untagged/
sh ../upload.sh
```

* Ensure index
```
use twitter
db.tweets_collection.ensureIndex({ t: "text" })
exit
```

290726 tweets unlocated, total 
* Dumping data from mongo: `mongodump --db test --collection tweets_collection -o /home/kaustubh/`

Data stored in .bson format in ~/test/

* Convert bson to json: `bsondump tweets_collection.bson > tweets_collection.json `
