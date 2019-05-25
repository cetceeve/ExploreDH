let Article = funktion(title, abstract, id) {
  this.title = title;
  this.abstract = abstract;
  this.id = id;

  this.authors = [];
  this.keywords = [];
};

export { Article };
