/* global ol */
/** 
 * Model for the map.
 * 
 * At the moment used to create/visualize a basic map and some test data.
 */

class Map {
  constructor() {
    this.tileLayer = this.initTileLayer();
    this.map = this.initMap(this.tileLayer);
    this.visualizePeopleAtLocation();
  }

  initTileLayer() {
    return new ol.layer.Tile({
      source: new ol.source.Stamen({
        layer: "toner",
      }),
    });
  }

  initMap(tileLayer) {
    return new ol.Map({
      target: "map",
      layers: [
        tileLayer,
      ],
      view: new ol.View({
        // center is set to Berlin [lon, lat]
        center: ol.proj.transform([13.41, 52.52], "EPSG:4326", "EPSG:3857"),
        zoom: 5.5,
      }),
    });
  }

  visualizePeopleAtLocation() {
    fetch(window.location.href + ":peopleAtLocation")
      .then(response => {
        if (response.status !== 200) {
          throw new Error("BadResponseCode: " + response.status.toString());
        }
        return response.json();
      })
      .then(data => {
        this.createNewLayer(data, this.map, this.tileLayer);
      })
      .catch(err => {
        // eslint-disable-next-line no-console
        console.error(err);
      });

  }

  createNewLayer(list, map, tileLayer) {
    let circles = [],
      vectorLayer,
      fill = new ol.style.Fill({ color: [180, 0, 0, 0.3] }),
      stroke = new ol.style.Stroke({ color: [180, 0, 0, 1], width: 1 }),
      style;

    for (let element of list) {
      circles.push(this.createCirclesFromData(element));
    }

    vectorLayer = new ol.layer.Vector({
      source: new ol.source.Vector({
        features: circles,
      }),
    });

    map.addLayer(vectorLayer);

    for (let element of circles) {
      element.getGeometry().transform(new ol.proj.Projection({ code: "EPSG:4326" }), tileLayer.getSource().getProjection());
    }

    style = new ol.style.Style({
      image: new ol.style.Circle({
        fill: fill,
        stroke: stroke,
      }),
      fill: fill,
      stroke: stroke,
    });
    vectorLayer.setStyle(style);
  }

  createCirclesFromData(data) {
    return new ol.Feature({
      geometry: new ol.geom.Circle([Number(data.lon), Number(data.lat)], Number(0.05 * data.numOfPeople)),
    });
  }

}

export default new Map();
