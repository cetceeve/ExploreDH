/* global d3 */

/** 
 * Model for the map.
 */

import config from "./config.js";

class Map {
    constructor() {
        this.mapSvg = d3.select("svg");
        this.projection = d3.geoMercator()
            .scale(1700)            // This is like the zoom
            .center([10, 50]);      // trial-and-error-result: no idea what this exactly does!

        this.initMap();
    }

    initMap() {
        d3.json("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson", data => {

            this.mapSvg.append("g")
                .selectAll("path")
                .data(data.features)
                .enter().append("path")
                .attr("fill", config.COUNTRIES)
                .attr("d", d3.geoPath()
                    .projection(this.projection)
                )
                .style("stroke", config.COUNTRY_BORDERS);

            // this.visualizePeopleAtLocation();
            this.visualizeAllConnections();
        });
    }

    visualizePeopleAtLocation() {
        fetch(window.location.href + "connections/peoplePerOrga")
            .then(response => {
                if (response.status !== 200) {
                    throw new Error("BadResponseCode: " + response.status.toString());
                }
                return response.json();
            })
            .then(data => {
                this.drawCirclesFromData(data);
            })
            .catch(err => {
                // eslint-disable-next-line no-console
                console.error(err);
            });
    }

    visualizeAllConnections() {
        fetch(window.location.href + "connections")
            .then(response => {
                if (response.status !== 200) {
                    throw new Error("BadResponseCode: " + response.status.toString());
                }
                return response.json();
            })
            .then(data => {
                this.drawNetworkPaths(data);
            })
            .catch(err => {
                // eslint-disable-next-line no-console
                console.error(err);
            });
    }

    visualizeArticleConnections() {
        fetch(window.location.href + "connections/connectionsOnArticle")
            .then(response => {
                if (response.status !== 200) {
                    throw new Error("BadResponseCode: " + response.status.toString());
                }
                return response.json();
            })
            .then(data => {
                this.drawNetworkPaths(data);
            })
            .catch(err => {
                // eslint-disable-next-line no-console
                console.error(err);
            });
    }

    drawCirclesFromData(data) {
        // visualize people at location
        this.mapSvg.selectAll("myCircles")
            .data(data)
            .enter()
            .append("circle")
            // .attr("id", d => d.id)
            .attr("cx", d => this.projection([d.lon, d.lat])[0])
            .attr("cy", d => this.projection([d.lon, d.lat])[1])
            .attr("r", d => d.numOfPeople)
            .style("fill", config.PEOPLE_AT_LOCATION)
            .attr("fill-opacity", 0.6);

        this.drawMarkerFromData(data);
    }

    drawMarkerFromData(data) {
        this.mapSvg.selectAll("myCircles")
            .data(data)
            .enter()
            .append("circle")
            .attr("id", d => d.id) // ================ id is undefined!! ==============================
            .attr("cx", d => this.projection([d.lon, d.lat])[0])
            .attr("cy", d => this.projection([d.lon, d.lat])[1])
            .attr("r", d => 3.5)
            .attr("uk-tooltip", d => "title: " + d.name + "; pos: right")
            .style("fill", config.MARKER_LOCATION)
            .on("click", d => {
                console.log("CLICKED" + d.id);
            })
            .on("pointerenter", (d, i, nodes) => {
                console.log("HOVERED");
                this.highlightConnectionsOfLocation("." + d.id, true);
                this.highlightMarker("#" + d.id, true);
            })
            .on("pointerout", (d, i, nodes) => {
                this.highlightConnectionsOfLocation("." + d.id, false);
                this.highlightMarker("#" + d.id, false);
            });

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
        // console.log(link);

        let pathGenerator = d3.geoPath()
            .projection(this.projection);

        this.mapSvg.selectAll("myPath")
            .data(link)
            .enter()
            .append("path")
            .attr("d", (d, i, nodes) => {

                //console.log(nodes[i]); // get current node
                //console.log(d);
                //nodes[i].classList.add("test"); // instead of test: add sourceId and targetId to classList
                nodes[i].classList.add(d.sourceId);
                nodes[i].classList.add(d.targetId);

                return pathGenerator(d);
            })
            .attr("stroke-opacity", 0.5)
            .style("fill", "none")
            .style("stroke", config.NETWORK_LINES)
            .style("stroke-width", 2);

        this.visualizePeopleAtLocation();
    }

    highlightConnectionsOfLocation(selector, highlight) {
        let selection = d3.selectAll(selector);
        // console.log(selection);

        if (highlight) {
            selection.style("stroke", "#00f");
        } else {
            selection.style("stroke", config.NETWORK_LINES);
        }
    }

    highlightMarker(selector, highlight) {
        let selection = d3.selectAll(selector);

        if (highlight) {
            selection.style("fill", "#0f0");
        } else {
            selection.style("fill", config.MARKER_LOCATION);
        }
    }
}

export default new Map();
