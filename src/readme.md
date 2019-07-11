# ExploreDH Website Code

## Server
- `index.js`: express server application serving the `/www` folder as the client code. It offers multiple routes for data requests:
  - `/connections`: provides the Orga Network from the `/data/output` folder
  - `/connections/peoplePerOrga`: provides the amount of people working at one organisation

### Building
- `build.js`: simple build script: copys all code necessary for live operation to the build folder
- `package.json`: we use npm as a build tool. This file contains multiple build scripts.

## Client
- `config.js`: file with configuration variables
- `map_d3.js`: visualization code. Provides a geoJSON map with markers and connections