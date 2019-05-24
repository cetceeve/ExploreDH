let Organisation = funktion(name, id, lat, lon) {
  this.name = name;
  this.id = id;
  this.lat = lat;
  this.lon = lon;

  this.locations = [];
  this.authors = [];
};

export { Organisation };
