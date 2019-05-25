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

    ////////////////// add point+line

    var point_feature = new ol.Feature({});
    var point_geom = new ol.geom.Point(
      [20, 20]
    );
    point_feature.setGeometry(point_geom);
    var linestring_feature = new ol.Feature({
      geometry: new ol.geom.LineString(
        [[10, 20], [20, 10], [30, 20]]
      )
    });
    var vector_layer = new ol.layer.Vector({
      source: new ol.source.Vector({
        features: [point_feature, linestring_feature]
      })
    })
    map.addLayer(vector_layer);

    var features = [
      point_feature,
      linestring_feature
    ];

    function transform_geometry(element) {
      var current_projection = new ol.proj.Projection({ code: "EPSG:4326" });
      var new_projection = layer.getSource().getProjection();

      element.getGeometry().transform(current_projection, new_projection);
    }

    features.forEach(transform_geometry);

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








