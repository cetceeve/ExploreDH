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
    if (req.params.request === "peoplePerOrga") {
        db.all("SELECT orga.lat, orga.lon, orga.name, count(person.id) AS numOfPeople FROM orga INNER JOIN person ON person.orga=orga.id GROUP BY orga.id ORDER BY numOfPeople", function (err, rows) {
            if (err !== null) {
                console.error(err);
            } else {
                console.log("sending data upstream");
                res.json(rows);
            }
        });
    }
    // test article: 49d0865a-9983-11e9-91b8-54ee75fb08ef
    if (req.params.request === "connectionsOnArticle") {
        db.all("SELECT DISTINCT orga.lat, orga.lon FROM orga INNER JOIN person ON person.orga=orga.id INNER JOIN article_person_link AS link ON person.id=link.person_id INNER JOIN article on link.article_id=article.id WHERE article.id=\"49d0865a-9983-11e9-91b8-54ee75fb08ef\"", function (err, rows) {
            if (err !== null) {
                console.error(err);
            } else {
                let data = [];
                for (let i = 0; i < rows.length; i++) {
                    for (let j = i + 1; j < rows.length; j++) {
                        data.push([rows[i], rows[j]]);
                    }
                }
                console.log("sending data upstream");
                res.json(data);
            }
        });
    }
});