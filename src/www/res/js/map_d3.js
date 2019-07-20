/* global d3 */

import config from "./config.js";

class Map extends EventTarget {
    constructor() {
        super();
        this.mapSvg = d3.select("svg");
        this.projection = d3.geoMercator()
            // This is like the zoom    
            .scale(config.SCALE)
            // trial-and-error-result: no idea what this exactly does!
            .center(config.CENTER);

        this.pointData = null;
        this.clicked = false;
        this.initMap();
    }

    initMap() {
        let participatingCountries = ["Germany", "France", "Italy", "Switzerland", "Austria", "Luxembourg"];

        d3.json("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson", data => {

            this.mapSvg.append("g")
                .selectAll("path")
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
            .attr("fill-opacity", config.PEOPLE_AT_LOCATION_OPACITY);

        this.fetchAllConnections();
    }

    drawMarkerFromData(data) {

        this.mapSvg.selectAll("myCircles")
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
                this.clicked = true;
                super.dispatchEvent(this.createEvent("onMarkerClicked", { id: d.id, name: d.name }));
            })
            .on("pointerenter", d => {
                this.highlightConnectionsOfLocation("." + d.id, true);
            })
            .on("pointerout", d => {
                if (!this.clicked) {
                    this.highlightConnectionsOfLocation("." + d.id, false);
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

        this.mapSvg.selectAll("myPath")
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

    highlightConnectionsOfLocation(selector, highlight) {
        let selection = d3.selectAll(selector);

        if (highlight) {
            selection
                .style("stroke", d => {
                    this.highlightMarker("#" + d.sourceId, true);
                    this.highlightMarker("#" + d.targetId, true);
                    return config.ACCENT;
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

    resetLocation(orgaId) {
        this.clicked = false;
        this.highlightConnectionsOfLocation("." + orgaId, false);
    }

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

    async _getData(url = "") {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error("BadResponseCode: " + response.status.toString());
        }
        return await response.json();
    }
}

export default new Map();
