/* global d3 */

import config from "./config.js";

class Map extends EventTarget {
  constructor() {
    super();
    this.mapContainerEl = document.getElementById("mapContainer");
    this.mapWidth = this.mapContainerEl.offsetWidth;
    this.mapHeight = this.mapContainerEl.offsetHeight;

    this.mapSvg = d3.select("svg")
      .attr("width", this.mapWidth)
      .attr("height", this.mapHeight);

    this.mapLayer = this.mapSvg.append("g");
    this.mapSvg.call(d3.zoom()
      .scaleExtent(config.SCALE_EXTENT)
      .on("zoom", () => {
        this.mapLayer.attr("transform", d3.event.transform);
      }));

    this.projection = d3.geoMercator()
      .scale(config.SCALE)
      .translate([this.mapWidth / config.TRANSLATION_FACTOR, this.mapHeight / config.TRANSLATION_FACTOR])
      .center(config.CENTER);

    this.pointData = null;
    this.clicked = false;
    this.clickedId = "";
    this.drawMap();
  }

  ///////////////////////////////////////////////////////////
  // functions to fetch data from db

  fetchPeopleAtLocation() {
    this._getData("connections/peoplePerOrga")
      .then(data => {
        this.drawCirclesFromData(data);
      })
      // eslint-disable-next-line no-console
      .catch(err => console.error(err));
  }

  fetchAllConnections() {
    this._getData("connections")
      .then(data => {
        this.drawNetworkPaths(data);
      })
      // eslint-disable-next-line no-console
      .catch(err => console.error(err));
  }

  fetchArticleConnections() {
    this._getData("connections/connectionsOnArticle")
      .then(data => {
        this.drawNetworkPaths(data);
      })
      // eslint-disable-next-line no-console
      .catch(err => console.error(err));
  }

  async _getData(url = "") {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error("BadResponseCode: " + response.status.toString());
    }
    return await response.json();
  }

  ///////////////////////////////////////////////////////////
  // functions to draw map and map elements

  drawMap() {
    let participatingCountries = ["Germany", "France", "Italy", "Switzerland", "Austria", "Luxembourg", "Russia", "Norway", "Canada"];

    d3.json("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson", data => {
      this.mapLayer.selectAll("path")
        .data(data.features)
        .enter().append("path")
        .attr("fill", config.COUNTRIES)
        .attr("opacity", d => {
          if (participatingCountries.includes(d.properties.name)) {
            return 1;
          }
          return config.NOT_PARTICIPATING_OPACITY;
        })
        .attr("d", d3.geoPath()
          .projection(this.projection)
        )
        .style("stroke", config.COUNTRY_BORDERS);

      this.fetchPeopleAtLocation();
    });
  }

  // visualize people at location
  drawCirclesFromData(data) {
    this.pointData = data;

    this.mapLayer.selectAll("myCircles")
      .data(data)
      .enter()
      .append("circle")
      .attr("cx", d => this.projection([d.lon, d.lat])[0])
      .attr("cy", d => this.projection([d.lon, d.lat])[1])
      .attr("r", d => config.MARKER_LOCATION_RADIUS + d.numOfPeople)
      .style("fill", config.PEOPLE_AT_LOCATION)
      .attr("fill-opacity", config.PEOPLE_AT_LOCATION_OPACITY);

    this.fetchAllConnections();
  }

  drawMarkerFromData(data) {
    this.mapLayer.selectAll("myCircles")
      .data(data)
      .enter()
      .append("circle")
      .attr("id", d => d.id)
      .attr("cx", d => this.projection([d.lon, d.lat])[0])
      .attr("cy", d => this.projection([d.lon, d.lat])[1])
      .attr("r", () => config.MARKER_LOCATION_RADIUS)
      .attr("title", d => d.name)
      .attr("class", "marker")
      .style("fill", config.MARKER_LOCATION)
      .on("click", d => {
        if (this.clicked) {
          this.resetLocation(this.clickedId);
        }
        this.clicked = true;
        this.clickedId = d.id;
        this.highlightMarker("#" + d.id, true, config.ACTIVE);
        super.dispatchEvent(this.createEvent("onMarkerClicked", { id: d.id, name: d.name }));
      })
      .on("pointerenter", d => {
        this.highlightConnectionsOfLocation("." + d.id, true);
        this.highlightMarker("#" + d.id, true);
      })
      .on("pointerout", d => {
        if (!this.clicked || this.clickedId !== d.id) {
          this.highlightConnectionsOfLocation("." + d.id, false);
          this.highlightMarker("#" + d.id, false);
        }
        if (this.clickedId === d.id) {
          this.highlightMarker("#" + d.id, true, config.ACTIVE);
        }
      })
      .append("svg:title")
      .text(d => d.name);

  }

  drawNetworkPaths(data) {
    // process data: coordinates of start and end
    var link = [];
    for (let row of data) {
      link.push({
        type: "LineString",
        coordinates: [
          [row[0].lon, row[0].lat],
          [row[1].lon, row[1].lat],
        ],
        sourceId: row[0].id,
        targetId: row[1].id,
      });
    }

    let pathGenerator = d3.geoPath()
      .projection(this.projection);

    this.mapLayer.selectAll("myPath")
      .data(link)
      .enter()
      .append("path")
      .attr("d", (d, i, nodes) => {
        nodes[i].classList.add(d.sourceId);
        nodes[i].classList.add(d.targetId);
        return pathGenerator(d);
      })
      .attr("stroke-opacity", config.NETWORK_LINES_OPACITY)
      .style("fill", "none")
      .style("stroke", config.NETWORK_LINES)
      .style("stroke-width", config.NETWORK_LINES_STROKE_WIDTH);

    this.drawMarkerFromData(this.pointData);
  }

  ///////////////////////////////////////////////////////////
  // functions to highlight map elements on user actions

  highlightConnectionsOfLocation(selector, highlight) {
    let selection = d3.selectAll(selector);

    if (highlight) {
      selection
        .style("stroke", d => {
          this.highlightMarker("#" + d.sourceId, true);
          this.highlightMarker("#" + d.targetId, true);
          return config.HIGHLIGHT;
        })
        .attr("stroke-opacity", 1)
        .raise();
    } else {
      selection
        .style("stroke", d => {
          this.highlightMarker("#" + d.sourceId, false);
          this.highlightMarker("#" + d.targetId, false);
          return config.NETWORK_LINES;
        })
        .attr("stroke-opacity", config.NETWORK_LINES_OPACITY);
      d3.selectAll(".marker").raise();
    }
  }

  highlightMarker(selector, highlight, color) {
    let selection = d3.selectAll(selector);

    if (highlight) {
      selection
        .style("fill", color || config.HIGHLIGHT)
        .raise();
    } else {
      selection
        .style("fill", config.MARKER_LOCATION)
        .raise();
    }
  }

  ///////////////////////////////////////////////////////////
  // functions used in controller

  resetLocation(orgaId) {
    this.clicked = false;
    this.clickedId = "";
    this.highlightConnectionsOfLocation("." + orgaId, false);
    this.highlightMarker("#" + orgaId, false);
  }

  ///////////////////////////////////////////////////////////
  // helper functions

  createEvent(type, data, msg) {
    let event = new Event(type);
    if (data !== null && data !== undefined) {
      event.data = data;
    }
    if (msg !== null && msg !== undefined) {
      event.msg = msg;
    }
    return event;
  }
}

export default new Map();
