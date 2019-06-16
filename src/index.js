"use strict";

/**
 * This script creates a simple express application to serve
 * the content of "./www" statically via http://localhost
 */
const express = require("express"), PORT = 42024;

// Create express app
var app = express();

// Enable static serving of www directory
app.use(express.static("www"));

// Starting server on port <PORT>
app.listen(PORT);

// eslint-disable-next-line no-console
console.log("Server runing at http://localhost:" + PORT);