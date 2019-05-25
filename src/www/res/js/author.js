let Author = funktion(firstName, lastName, eMail, id) {
  this.firstName = firstName;
  this.lastName = lastName;
  this.eMail = eMail;
  this.id = id;

  this.articles = [];
  this.organisations = [];
};

export { Author };
