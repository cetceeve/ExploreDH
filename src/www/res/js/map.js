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

    let layer = new ol.layer.Tile({
      source: new ol.source.Stamen({
        layer: "toner"
      })
    });

    var map = new ol.Map({
      target: 'map',
      layers: [
        layer
      ],
      view: new ol.View({
        // set center to Berlin [lon, lat]
        center: ol.proj.transform([13.41, 52.52], 'EPSG:4326', 'EPSG:3857'),
        zoom: 4
      })
    });

    ////////////////// add point

    var point_feature = new ol.Feature({
      geometry: new ol.geom.Point([13.41, 52.52])
    });

    var circleFeature = new ol.Feature({
      geometry: new ol.geom.Circle([8.27, 49.98], 3)
    });

    var vector_layer = new ol.layer.Vector({
      source: new ol.source.Vector({
        features: [point_feature, circleFeature]
      })
    })
    map.addLayer(vector_layer);

    point_feature.getGeometry().transform(new ol.proj.Projection({ code: "EPSG:4326" }), layer.getSource().getProjection());
    circleFeature.getGeometry().transform(new ol.proj.Projection({ code: "EPSG:4326" }), layer.getSource().getProjection());

    var fill = new ol.style.Fill({
      color: [180, 0, 0, 0.3]
    });

    var stroke = new ol.style.Stroke({
      color: [180, 0, 0, 1],
      width: 1
    });

    var style = new ol.style.Style({
      image: new ol.style.Circle({
        fill: fill,
        stroke: stroke,
        radius: 8
      }),
      fill: fill,
      stroke: stroke
    });
    vector_layer.setStyle(style);


  }
}


export default new Map();








