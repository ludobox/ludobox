var jsf = require('json-schema-faker');
var schema = require('../../ludobox/model/schema');
var jsonfile = require('jsonfile');
var slugify = require('slugify')
var fs = require('fs');

var ROOT_DIR = '../../data/';


function createSampleGame() {
  var sample = jsf(schema);
  var slug = slugify(sample.title).toLowerCase();

  var dir = ROOT_DIR+slug;

  if (!fs.existsSync(dir)){
      fs.mkdirSync(dir);
  }

  var file = dir + "/info.json"

  jsonfile.writeFile(file, sample, function (err) {
    if (err) throw(err)
    console.log('Sample file saved at '+file)
  })
}

for (var i = 0; i < 10; i++) {
  createSampleGame()
}
