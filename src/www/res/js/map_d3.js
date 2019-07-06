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

            this.visualizePeopleAtLocation();
            this.visualizeConnections();
        });
    }

    visualizePeopleAtLocation() {
        fetch(window.location.href + "peoplePerOrga")
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

    visualizeConnections() {
        fetch(window.location.href + "connectionsOnArticle")
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
            .attr("id", d => d.id)
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
            .attr("id", d => d.id)
            .attr("cx", d => this.projection([d.lon, d.lat])[0])
            .attr("cy", d => this.projection([d.lon, d.lat])[1])
            .attr("r", d => 3.5)
            .style("fill", config.MARKER_LOCATION)
            .on("click", d => console.log("CLICKED" + d.id))
            .on("pointerenter", (d, i, nodes) => console.log("HOVERED"));

        // this.drawNetworkPaths();
    }

    drawNetworkPaths(data) {
        // Create test-data: coordinates of start and end
        var link = [];
        for (let row of data) {
            link.push({
                type: "LineString",
                coordinates: [
                    [row[0].lon, row[0].lat],
                    [row[1].lon, row[1].lat],
                ],
            });
        }
        // var link = [
        //     { type: "LineString", coordinates: [[12, 54], [-123, 48]] },
        //     { type: "LineString", coordinates: [[-123, 48], [9, 52]] },
        //     { type: "LineString", coordinates: [[9, 52], [6, 46]] },
        //     { type: "LineString", coordinates: [[6, 46], [13, 52]] },
        //     { type: "LineString", coordinates: [[13, 52], [7, 46]] },
        //     { type: "LineString", coordinates: [[7, 46], [11, 44]] },
        //     { type: "LineString", coordinates: [[11, 44], [5, 50]] },
        //     { type: "LineString", coordinates: [[5, 50], [8, 49]] }
        // ];

        let pathGenerator = d3.geoPath()
            .projection(this.projection);

        this.mapSvg.selectAll("myPath")
            .data(link)
            .enter()
            .append("path")
            .attr("d", d => pathGenerator(d))
            .style("fill", "none")
            .style("stroke", config.NETWORK_LINES)
            .style("stroke-width", 2);
    }
}

export default new Map();
