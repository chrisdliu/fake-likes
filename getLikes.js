"use strict";

function sleep(sleepDuration){
    var now = new Date().getTime();
    while(new Date().getTime() < now + sleepDuration){ /* do nothing */ } 
}

var cheerio = require('cheerio');
var fs = require('fs');
var login = require("./js/index");


if (process.argv.length != 6) {
  console.error("Must supply 4 args!");
  process.exit(1);
}

var input = process.argv[2];
var output = process.argv[3];
var email = process.argv[4];
var password = process.argv[5];


async function writeLikes(profiles, data, api) {
  if (profiles.length == 0) {
    fs.writeFile(output, JSON.stringify(data), 'utf8', (err) => {
      if (err) throw err;
    });
  } else {
    var profile = profiles[0];

    var url = 'https://m.facebook.com/' + profile['id'] + '?v=likes';
    var time = Math.random() * 3000 + 4000;
    sleep(time);

    var response = await api.getProfileLikes(url, sleep);
    var $ = cheerio.load(response['body']);
    var likes = parseInt($('div').filter(function() { 
      return $(this).text() === 'All Likes';
    }).prev().text());
    console.log(profile['id'] + ' | ' + likes);

    var d = {};
    d[profile['id']] = likes;
    data.push(d);

    writeLikes(profiles.slice(1), data, api);
  }
}


login({email: email, password: password}, (err, api) => {
  if (err) return console.error(err);

  var profiles = JSON.parse(fs.readFileSync(input));

  writeLikes(profiles, [], api);
});

