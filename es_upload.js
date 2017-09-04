var elasticsearch = require('elasticsearch'),
    fs = require('fs'),
    pubs = JSON.parse(fs.readFileSync('xaa')); // name of my first file to parse
var client = new elasticsearch.Client({  // default is fine for me, change as you see fit
  host: 'localhost:9200',
  log: 'trace'
});

for (var i = 0; i < pubs.length; i++ ) {
  client.create({
    index: "twitter", // name your index
    type: "twitter type", // describe the data thats getting created
    id: i, // increment ID every iteration - I already sorted mine but not a requirement
    body: pubs[i] // *** THIS ASSUMES YOUR DATA FILE IS FORMATTED LIKE SO: [{prop: val, prop2: val2}, {prop:...}, {prop:...}] - I converted mine from a CSV so pubs[i] is the current object {prop:..., prop2:...}
  }, function(error, response) {
    if (error) {
      console.error(error);
      return;
    }
    else {
    console.log(response);  //  I don't recommend this but I like having my console flooded with stuff.  It looks cool.  Like I'm compiling a kernel really fast.
    }
  });
}

// source: https://stackoverflow.com/a/25218368/7727071
