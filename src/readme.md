# ExploreDH Website Code

> for more information on the scripts read src/scripts/readme.md

## Server
- `index.js`: express server application serving the `/www` folder as the client code. It offers multiple GET-routes for data requests:
  - `/connections`: provides the Orga Network from the `/data/output` folder
  - `/connections/peoplePerOrga`: provides the amount of people working at one organisation
  - `/connections/connectionsOnArticle/:articleID`: provides all connections for one article by articleID
  - `/search`: provides id and title of all articles for the autocomplete suggestions in the search bar
  - `/article/:id`: provides one article in a format where all IDs are replaced with the actual data
  - `/article/articleByOrga/:orgaID`: provides all article by one organisation in a format where all IDs are replaced with the actual data


### Building
- `build.js`: simple build script: copys all code necessary for live operation to the build folder
- `package.json`: we use npm as a build tool. This file contains multiple build scripts.

## Client
- `config.js`: file with configuration variables
- `controller.js`: handles communication between map and sidebar
- `map_d3.js`: map component. Provides an interactable geoJSON map with markers and connections
- `article_sidebar.js`: sidebar component. displays articles and provides a searchbar with autocomplete suggestions