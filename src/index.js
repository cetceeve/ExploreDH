"use strict";

/**
 * This script creates a simple express application to serve
 * the content of "./www" statically via http://localhost
 */
const express = require("express"), PORT = 5012,
    sqlite3 = require("sqlite3").verbose();

var app = express(),
    db = new sqlite3.Database("../data/db/dhd_data.db", sqlite3.OPEN_READONLY, (err) => {
        if (err !== null) {
            console.error(err);
        }
    });

app.use(express.static("www"));
app.listen(PORT);
console.log("Server runing at http://localhost:" + PORT);

app.get("/:request", function (req, res) {
    console.log(req.params);
    if (req.params.request === "peopleAtLocation") {
        db.all("SELECT city.lat, city.lon, count(person.id) AS numOfPeople FROM person INNER JOIN orga ON person.orga=orga.id INNER JOIN city ON orga.city=city.id GROUP BY city.id", function (err, rows) {
            if (err !== null) {
                console.error(err);
            } else {
                console.log("sending data upstream");
                res.json(rows);
            }
        });
    }
    if (req.params.request === "keyword") {
        let query = `SELECT city.lat, city.lon, count(keyword.id) AS numOfPeople FROM article INNER JOIN article_person_link AS link ON article.id=link.article_id INNER JOIN person ON link.person_id=person.id INNER JOIN orga ON person.orga=orga.id INNER JOIN city ON orga.city=city.id INNER JOIN article_keyword_link AS link2 ON link2.article_id=article.id INNER JOIN keyword ON keyword.id=link2.keyword_id WHERE keyword.text="${req.query.name}" GROUP BY city.id`;
        db.all(query, function (err, rows) {
            if (err !== null) {
                console.error(err);
            } else {
                console.log("sending data upstream");
                res.json(rows);
            }
        });
    }
});