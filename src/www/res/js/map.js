/** 
 * Model for the map.
 * 
 * At the moment used to create/visualize a basic map.
 */

class Map {
  constructor() {
    this.initMap();
  }


  initMap() {
    var map = new ol.Map({
      target: 'map',
      layers: [
        new ol.layer.Tile({
          source: new ol.source.Stamen({
            layer: "toner"
          })
        })
      ],
      view: new ol.View({
        // set center to Berlin
        center: ol.proj.transform([13.41, 52.52], 'EPSG:4326', 'EPSG:3857'),
        zoom: 4
      })
    });
  }
}

export default new Map();








