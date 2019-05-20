/** 
 * Model for the map.
 * 
 * At the moment used to create/visualize a basic map.
 */

 class Map {
   constructor() {
     //super(); -- throws error: "SyntaxError: super() is only valid in derived class constructors"
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
      center: ol.proj.fromLonLat([37.41, 8.82]),
      zoom: 4
    })
  });
}
 }

 export default new Map();






   

 