"use strict";

/**
 * This script creates a simple express application to serve
 * the content of "./www" statically via http://localhost
 */
const express = require("express"), PORT = 42024,
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

app.get("/:test", function (req, res) {
    console.log(req.params);
    res.send("zimzalabim");
    getData();
});

function getData() {
    db.all("SELECT loc.lat, loc.lon, count(person.id) AS numOfPeople FROM person INNER JOIN orga ON person.orga=orga.id INNER JOIN location as loc ON orga.location=loc.id GROUP BY loc.id", function (err, rows) {
        if (err !== null) {
            console.error(err);
        }
        console.log(rows);
    });
}