var jsf = require('json-schema-faker');
var schema = require('../../ludobox/model/schema');
var jsonfile = require('jsonfile');
var slugify = require('slugify')
var fs = require('fs');

var ROOT_DIR = '../../data/';


function writeFile(dir) {
  var filename = Math.random().toString(36).substring(7);

  var filepath = dir+"/"+filename;

  fs.writeFile(filepath, "Hey there!", function(err) {
    if(err) {
        return console.log(err);
    }
    console.log("-- file saved! : " + filepath);
  });
}

function writeRandomFiles(dir) {
  for (var i = 0; Math.floor(Math.random()*10); i++) {
    writeFile(dir)
  }
}

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
    console.log('Sample info file saved at '+file)

    if (fs.existsSync(dir)){
        fs.mkdirSync(dir+"/files");
        writeRandomFiles(dir+"/files")
    }

  })
}

for (var i = 0; i < 10; i++) {
  createSampleGame()
}
