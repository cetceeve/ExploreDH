/*jshint esversion: 6 */
/** 
 * Model for the map.
 * 
 * At the moment used to create/visualize a basic map and some test data.
 */

class Map {
    constructor() {
        // The svg
        this.mapSvg = d3.select("svg");
        this.projection = d3.geoMercator()
            .scale(1700)            // This is like the zoom
            .center([10, 50]);      // trial-and-error-result: no idea what this exactly does!

        this.initMap();
    }

    initMap() {

        // Load external data and boot
        d3.json("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson", data => {

            // Draw the map
            this.mapSvg.append("g")
                .selectAll("path")
                .data(data.features)
                .enter().append("path")
                .attr("fill", "#718093")
                .attr("d", d3.geoPath()
                    .projection(this.projection)
                )
                .style("stroke", "#f5f6fa");

            this.visualizePeopleAtLocation();
        });
    }

    visualizePeopleAtLocation() {
        fetch(window.location.href + "peopleAtLocation")
            .then(response => {
                if (response.status !== 200) {
                    throw new Error("BadResponseCode: " + response.status.toString());
                }
                return response.json();
            })
            .then(data => {
                this.drawCircles(data);
            })
            .catch(err => {
                // eslint-disable-next-line no-console
                console.error(err);
            });
    }

    drawCircles(data) {
        console.log(data);
        // visualize people at location
        this.mapSvg.selectAll("myCircles")
            .data(data)
            .enter()
            .append("circle")
            .attr("id", d => d.id)
            .attr("cx", d => this.projection([d.lon, d.lat])[0])
            .attr("cy", d => this.projection([d.lon, d.lat])[1])
            .attr("r", d => d.numOfPeople)
            .attr("stroke", "#c23616")
            .attr("stroke-width", 2)
            .attr("fill-opacity", 0.4);

        // visualize marker at location
        this.mapSvg.selectAll("myGs")
            .data(data)
            .enter()
            .append("g")
            .attr("id", d => d.name) // has actually no name
            .attr("transform", d => "translate(" + this.projection([d.lon, d.lat]) + ")")
            .append("path")
            .attr("d", "M 100 100 L 300 100 L 200 300 z")
            .attr("transform", "scale(0.05) translate(-200,-300)") // trial-and-error-result: no idea what this exactly does!
            .style("fill", "#000")
            .on("click", d => console.log("CLICKED"))
            .on("pointerenter", (d, i, nodes) => console.log("HOVERED"));

        this.visualizeNetwork();
    }

    visualizeNetwork() {
        // Create data: coordinates of start and end
        var link = [
            { type: "LineString", coordinates: [[12, 54], [-123, 48]] },
            { type: "LineString", coordinates: [[-123, 48], [9, 52]] },
            { type: "LineString", coordinates: [[9, 52], [6, 46]] },
            { type: "LineString", coordinates: [[6, 46], [13, 52]] },
            { type: "LineString", coordinates: [[13, 52], [7, 46]] },
            { type: "LineString", coordinates: [[7, 46], [11, 44]] },
            { type: "LineString", coordinates: [[11, 44], [5, 50]] },
            { type: "LineString", coordinates: [[5, 50], [8, 49]] }
        ];

        // A path generator
        var path = d3.geoPath()
            .projection(this.projection);

        // Add the path
        this.mapSvg.selectAll("myPath")
            .data(link)
            .enter()
            .append("path")
            .attr("d", d => path(d))
            .style("fill", "none")
            .style("stroke", "orange")
            .style("stroke-width", 2);
    }

}

export default new Map();
