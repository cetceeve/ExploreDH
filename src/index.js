"use strict";

/**
 * This script creates a simple express application to serve
 * the content of "./www" statically via http://localhost
 */
const express = require("express"),
  PORT = 5012,
  sqlite3 = require("sqlite3").verbose(),
  fs = require("fs"),
  conns = JSON.parse(fs.readFileSync("../data/output/output_orga_network.json")),
  jsonDB = JSON.parse(fs.readFileSync("../data/output/output_database.json"));

var app = express(),
  db = new sqlite3.Database("../data/db/dhd_data.db", sqlite3.OPEN_READONLY, (err) => { if (err) { console.error(err); } });

app.use(express.static("www"));
app.listen(PORT);
console.log("Server runing at http://localhost:" + PORT);

app.get("/connections", function (req, res) {
  console.log("sending connections upstream");
  res.json(conns);
});

app.get("/connections/peoplePerOrga", function (req, res) {
  db.all("SELECT orga.id, orga.lat, orga.lon, orga.name, count(person.id) AS numOfPeople FROM orga INNER JOIN person ON person.orga=orga.id GROUP BY orga.id ORDER BY numOfPeople", function (err, rows) {
    if (err) { console.error(err); } else {
      console.log("sending peoplePerOrga upstream");
      res.json(rows);
    }
  });
});

app.get("/connections/connectionsOnArticle/:articleID", function (req, res) {
  console.log(req.url + req.params);
  db.all("SELECT DISTINCT orga.id, orga.lat, orga.lon FROM orga INNER JOIN person ON person.orga=orga.id INNER JOIN article_person_link AS link ON person.id=link.person_id INNER JOIN article on link.article_id=article.id WHERE article.id=$id", { $id: req.params.arcticleID }, function (err, rows) {
    if (err) { console.error(err); } else {
      // create connections
      let data = [];
      for (let i = 0; i < rows.length; i++) {
        for (let j = i + 1; j < rows.length; j++) {
          data.push([rows[i], rows[j]]);
        }
      }
      console.log("sending connectionsOnArticle upstream");
      res.json(data);
    }
  });
});

app.get("/search", function (req, res) {
  db.all("SELECT id, title FROM article", function (err, rows) {
    if (err) { console.error(err); } else {
      console.log("sending search options upstream");
      res.json(rows);
    }
  });
});

app.get("/article/:id", function (req, res) {
  console.log(req.url + req.params);
  console.log("sending article upstream");
  res.json(buildArticleForDisplay(req.params.id));
});

app.get("/article/articleByOrga/:orgaID", function (req, res) {
  console.log(req.url + req.params);
  db.all("SELECT DISTINCT article.id FROM article INNER JOIN article_person_link AS link ON article.id=link.article_id INNER JOIN person on link.person_id=person.id INNER JOIN orga ON person.orga=orga.id WHERE orga.id=$id", { $id: req.params.orgaID }, function (err, rows) {
    if (err) { console.error(err); } else {
      let data = [];
      for (let item of rows) {
        data.push(buildArticleForDisplay(item.id));
      }
      console.log("sending article upstream");
      res.json(data);
    }
  });
});

function buildArticleForDisplay(articleID) {
  let article = jsonDB.articles[articleID];
  return {
    id: article.id,
    title: article.title,
    authors: article.authors.map(authorID => jsonDB.people[authorID].firstName + " " + jsonDB.people[authorID].lastName),
    keywords: article.keywords.map(keywordID => jsonDB.keywords[keywordID].text),
  };
}
