/** 
 * Model for the map.
 * 
 * At the moment used to create/visualize a basic map and some test data.
 */

class Map {
  constructor() {
    this.map;
    this.tileLayer;
    this.initMap();

    // test data (lon+lat from dhd)
    this.testList = [
      { lon: 8.27, lat: 49.98, radius: 1 }, // Mainz
      { lon: 7.16, lat: 51.27, radius: 2 }, // Wuppertal
      { lon: 13.41, lat: 52.5, radius: 3 } // Berlin
    ];

    this.createNewLayer(this.testList, this.map, this.tileLayer);
  }


  initMap() {
    this.tileLayer = new ol.layer.Tile({
      source: new ol.source.Stamen({
        layer: "toner"
      })
    });

    this.map = new ol.Map({
      target: 'map',
      layers: [
        this.tileLayer
      ],
      view: new ol.View({
        // center is set to Berlin [lon, lat]
        center: ol.proj.transform([13.41, 52.52], 'EPSG:4326', 'EPSG:3857'),
        zoom: 4
      })
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
        features: circles
      })
    });

    map.addLayer(vectorLayer);

    for (let element of circles) {
      element.getGeometry().transform(new ol.proj.Projection({ code: "EPSG:4326" }), tileLayer.getSource().getProjection());
    }

    style = new ol.style.Style({
      image: new ol.style.Circle({
        fill: fill,
        stroke: stroke
      }),
      fill: fill,
      stroke: stroke
    });
    vectorLayer.setStyle(style);
  }

  createCirclesFromData(data) {
    return new ol.Feature({
      geometry: new ol.geom.Circle([data.lon, data.lat], data.radius)
    });
  }

}

export default new Map();
