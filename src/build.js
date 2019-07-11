/* eslint-env node */
"use strict";

/**
 * This script builds and deplos the ExploreDH app to OUTPUT_DIR
 *
 * Tasks:
 * 	- Remove existsing build directory
 * 	- Create empty build directoy
 * 	- Copy necessary files from www/ to build directory
 *
 */

const fs = require("fs-extra"), // [https://github.com/jprichardson/node-fs-extra]
  OUTPUT_DIR = "build";

function log(msg) {
  // eslint-disable-next-line no-console
  console.log(msg);
}

log("Building ExploreDH-App");

// Remove current output dir if exists
if (fs.existsSync(OUTPUT_DIR)) {
  log("Removing existing output dir");
  fs.removeSync(OUTPUT_DIR);
}

// Create output dir
log("(Re-)create output dir");
fs.mkdirSync(OUTPUT_DIR);

// Copy client and server
log("Copying files");
fs.copySync("www/", OUTPUT_DIR + "/src/www");
fs.copySync("index.js", OUTPUT_DIR + "/src/index.js");
fs.copySync("package.json", OUTPUT_DIR + "/src/package.json");
fs.copySync("../data/db", OUTPUT_DIR + "/data/db");
fs.copySync("../data/output", OUTPUT_DIR + "/data/output");
