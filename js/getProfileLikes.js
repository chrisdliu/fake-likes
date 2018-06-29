"use strict";

var utils = require("./utils");
var fs = require('fs');
var log = require("npmlog");

module.exports = function(defaultFuncs, api, ctx) {
  return function getProfileLikes(url, callback) {
    if (!callback) {
      throw { error: "getPage: need callback" };
    }

    return defaultFuncs
      .get(url, ctx.jar)
      .catch(function(err) {
        log.error("getProfileLikes", err);
      });
  };
};
