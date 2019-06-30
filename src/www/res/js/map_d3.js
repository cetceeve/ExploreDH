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
            .scale(1250)            // This is like the zoom
            .center([10, 50]);      // trial-and-error-Result: no idea what this exactly does!

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
            .attr("stroke-width", 1)
            .attr("fill-opacity", .4);

        // visualize marker at location
        this.mapSvg.selectAll("myGs")
            .data(data)
            .enter()
            .append("g")
            .attr("id", d => d.name) // has actually no name
            .attr("transform", d => "translate(" + this.projection([d.lon, d.lat]) + ")")
            .append("path")
            .attr("d", 'M 100 100 L 300 100 L 200 300 z')
            .attr('transform', 'scale(0.04) translate(-150,-130)')
            .style("fill", "#000")
            .on("click", d => console.log("CLICKED"))
            .on("pointerenter", (d, i, nodes) => console.log("HOVERED"));
    }

}

export default new Map();
