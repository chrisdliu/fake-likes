"use strict";

var utils = require("./utils");
var qs = require("query-string");
var log = require("npmlog");

module.exports = function(defaultFuncs, api, ctx) {
  return function getPageLikes(page_id, offset, limit, callback) {
    if (!callback) {
      throw { error: "getLikes: need callback" };
    }

    var url = "https://www.facebook.com/pages/admin/people_and_other_pages/entquery/";

    var querys = {
      query_edge_key: "PEOPLE_WHO_LIKE_THIS_PAGE",
      page_id: page_id,
      offset: offset,
      limit: limit,
    };

    defaultFuncs
      .post(url + "?" + qs.stringify(querys), ctx.jar, {})
      .then(utils.parseAndCheckLogin(ctx, defaultFuncs))
      .then(function(data) {
        callback(data);
      })
      .catch(function(err) {
        log.error("getLikes", err);
      });
  };
};
