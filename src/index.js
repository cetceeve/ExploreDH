"use strict";

/**
 * This script creates a simple express application to serve
 * the content of "./www" statically via http://localhost
 */
const express = require("express"), PORT = 5012,
    sqlite3 = require("sqlite3").verbose(),
    fs = require("fs");

var app = express(),
    db = new sqlite3.Database("../data/db/dhd_data.db", sqlite3.OPEN_READONLY, (err) => {
        if (err !== null) {
            console.error(err);
        }
    });

app.use(express.static("www"));
app.listen(PORT);
console.log("Server runing at http://localhost:" + PORT);

app.get("/connections/peoplePerOrga", function (req, res) {
    console.log(req.params);
    db.all("SELECT orga.lat, orga.lon, orga.name, count(person.id) AS numOfPeople FROM orga INNER JOIN person ON person.orga=orga.id GROUP BY orga.id ORDER BY numOfPeople", function (err, rows) {
        if (err !== null) {
            console.error(err);
        } else {
            console.log("sending peoplePerOrga upstream");
            res.json(rows);
        }
    });
});

app.get("/connections/connectionsOnArticle/:articleID", function (req, res) {
    console.log(req.params);
    db.all("SELECT DISTINCT orga.id, orga.lat, orga.lon FROM orga INNER JOIN person ON person.orga=orga.id INNER JOIN article_person_link AS link ON person.id=link.person_id INNER JOIN article on link.article_id=article.id WHERE article.id=$id", { $id: req.params.arcticleID }, function (err, rows) {
        if (err !== null) {
            console.error(err);
        } else {
            // create connections
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
});

app.get("/search", function (req, res) {
    console.log(req.url);
    db.all("SELECT title FROM article", function (err, rows) {
        if (err !== null) {
            console.error(err);
        } else {
            console.log("sending article names upstream");
            res.json(rows.map(item => item.title));
        }
    });
});

app.get("/search/:query", function (req, res) {
    console.log(req.params.query);
    db.all("SELECT article.title FROM article WHERE article.title LIKE $q", { $q: "%" + req.params.query + "%" }, function (err, rows) {
        if (err !== null) {
            console.error(err);
        } else {
            console.log("sending article names upstream");
            res.json(rows.map(item => item.title));
        }
    });
});

app.get("/article/:title", function (req, res) {
    console.log(req.params);
    db.get("SELECT * FROM article WHERE article.title=$title", { $title: req.params.title }, function (err, rows) {
        if (err !== null) {
            console.error(err);
        } else {
            console.log("sending article upstream");
            res.json(rows);
        }
    });
});

app.get("/article/articleByOrga/:orgaID", function (req, res) {
    console.log(req.params);
    db.get("SELECT * FROM article INNER JOIN article_person_link AS link ON article.id=link.article_id INNER JOIN person on link.person_id=person.id INNER JOIN orga ON person.orga=orga.id WHERE orga.id=$id GROUP BY orga.id", { $id: req.params.orgaID }, function (err, rows) {
        if (err !== null) {
            console.error(err);
        } else {
            console.log("sending articleByOrga upstream");
            res.json(rows);
        }
    });
});

app.get("/connections", function (req, res) {
    console.log(req.url);
    readJSON("../data/output/output_orga_network.json")
        .then(data => {
            console.log("sending connections upstream");
            res.json(data);
        })
        .catch(e => {
            console.error(e);
        });
});

function readJSON(path) {
    return new Promise((resolve, reject) => {
        try {
            let rawdata = fs.readFileSync(path);
            resolve(JSON.parse(rawdata));
        } catch (err) {
            reject(err);
        }
    });
}