/* global d3 */

import config from "./config.js";

class Map {
    constructor() {
        this.mapSvg = d3.select("svg");
        this.projection = d3.geoMercator()
            .scale(1700)            // This is like the zoom
            .center([10, 50]);      // trial-and-error-result: no idea what this exactly does!

        this.pointData = null;
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

            this.visualizePeopleAtLocation();
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
        this.pointData = data;

        // visualize people at location
        this.mapSvg.selectAll("myCircles")
            .data(data)
            .enter()
            .append("circle")
            .attr("cx", d => this.projection([d.lon, d.lat])[0])
            .attr("cy", d => this.projection([d.lon, d.lat])[1])
            .attr("r", d => d.numOfPeople)
            .style("fill", config.PEOPLE_AT_LOCATION)
            .attr("fill-opacity", 0.6);

        this.visualizeAllConnections();
    }

    drawMarkerFromData(data) {
        this.mapSvg.selectAll("myCircles")
            .data(data)
            .enter()
            .append("circle")
            .attr("id", d => d.id)
            .attr("cx", d => this.projection([d.lon, d.lat])[0])
            .attr("cy", d => this.projection([d.lon, d.lat])[1])
            .attr("r", d => 3.5)
            // .attr("uk-tooltip", d => "title: " + d.name + "; pos: right")
            .attr("title", d => d.name)
            .style("fill", config.MARKER_LOCATION)
            .on("click", d => {
                console.log("CLICKED" + d.id);
                // TODO: call "fetchArticlesOfOrga"
            })
            .on("pointerenter", d => this.highlightConnectionsOfLocation("." + d.id, true))
            .on("pointerout", d => this.highlightConnectionsOfLocation("." + d.id, false))
            // TOOLTIP =======================
            .append("svg:title")
            .text(function (d) {
                return d.name;
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

        let pathGenerator = d3.geoPath()
            .projection(this.projection);

        this.mapSvg.selectAll("myPath")
            .data(link)
            .enter()
            .append("path")
            .attr("d", (d, i, nodes) => {
                nodes[i].classList.add(d.sourceId);
                nodes[i].classList.add(d.targetId);

                return pathGenerator(d);
            })
            .attr("stroke-opacity", 0.5)
            .style("fill", "none")
            .style("stroke", config.NETWORK_LINES)
            .style("stroke-width", 2);

        this.drawMarkerFromData(this.pointData);
    }

    highlightConnectionsOfLocation(selector, highlight) {
        let selection = d3.selectAll(selector);

        if (highlight) {
            selection
                .style("stroke", d => {
                    this.highlightMarker("#" + d.sourceId, true);
                    this.highlightMarker("#" + d.targetId, true);
                    return config.ACCENT;
                })
                .attr("stroke-opacity", 1);
        } else {
            selection
                .style("stroke", d => {
                    this.highlightMarker("#" + d.sourceId, false);
                    this.highlightMarker("#" + d.targetId, false);
                    return config.NETWORK_LINES;
                })
                .attr("stroke-opacity", 0.5);
        }
    }

    highlightMarker(selector, highlight) {
        let selection = d3.selectAll(selector);

        if (highlight) {
            selection
                .style("fill", config.ACCENT)
                .raise();
        } else {
            selection
                .style("fill", config.MARKER_LOCATION)
                .raise();
        }
    }
}

export default new Map();
