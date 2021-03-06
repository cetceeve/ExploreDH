/* global autoComplete _ */

class ArticleSidebar extends EventTarget {
  constructor() {
    super();
    // initial state
    this.allArticles = [];
    this.searchChoices = [];
    this.currentOrgaId = "";
    this._initSearchAutocomplete(this);

    // set all articles as search choices
    this._fetchArticles();

    this.articleListEl = document.querySelector("#articleList");
    this.locationContainerEl = document.querySelector("#locationContainer");
    this.clearLocationButton = document.querySelector("#buttonClose");

    this.articleTemplate = _.template(
      "<div class='uk-card uk-card-default uk-card-body'>" +
      "<h3 class='uk-card-title cardHead'><%=title%></h3>" +
      "<p><%=authors.join(', ')%></p>" +
      "<div class='uk-card-footer keywords'>" +
      "<% for (let keyword in keywords) { %>" +
      "<span class='uk-badge badge'><%=keywords[keyword]%></span>" +
      "<% } %>" +
      "</div>" +
      "</div>"
    );
  }

  ///////////////////////////////////////////////////////////
  // functions used in controller

  setArticlesByOrga(orgaID) {
    this.currentOrgaId = orgaID;
    this._getData("article/articleByOrga/" + orgaID)
      .then(data => {
        this.showArticleList(data);
        this.setSearchChoices(data);
      })
      // eslint-disable-next-line no-console
      .catch(err => console.error(err));
  }

  setLocationName(name) {
    let locationNameEl = document.querySelector("#locationName");
    this.locationContainerEl.style.display = "block";
    this.locationContainerEl.style.visibility = "visible";
    locationNameEl.innerHTML = name;
    this.clearLocationButton.addEventListener("click", () => this.clearLocationName());
  }

  ///////////////////////////////////////////////////////////
  // functions to show and clear list of articles and search choices

  setSearchChoices(_choices) {
    if (!(_choices !== undefined && _choices !== null && _choices.length !== 0)) {
      this.searchChoices = this.allArticles;
    } else {
      this.searchChoices = _choices;
    }
  }

  showArticleList(articleList) {
    this.clearArticleListAndSearchChoices();

    this.articleListEl.scrollTop = 0;
    for (let entry of articleList) {
      let container = document.createElement("li"),
        articleHTML = this.articleTemplate(entry);

      container.innerHTML = articleHTML;
      container.id = entry.id;
      this.articleListEl.appendChild(container);
    }
  }

  clearArticleListAndSearchChoices() {
    while (this.articleListEl.firstChild) {
      this.articleListEl.removeChild(this.articleListEl.firstChild);
    }

    this.setSearchChoices(null);
  }

  clearLocationName() {
    this.locationContainerEl.style.visibility = "hidden";
    this.locationContainerEl.style.display = "none";
    this.clearArticleListAndSearchChoices();
    super.dispatchEvent(this.createEvent("onLocationReset", this.currentOrgaId));
  }

  ///////////////////////////////////////////////////////////
  // functions for search-autocopmlete

  _initSearchAutocomplete(that) {
    return new autoComplete({
      selector: "#search",
      minChars: 2,
      cache: false,
      source: function(term, suggest) {
        let re = RegExp(term.toLowerCase(), "gi");
        suggest(that.searchChoices.filter(item => re.test(item.title.toLowerCase())));
      },
      onSelect(event, term, item) {
        that._getData("article/" + item.dataset.id)
          .then(data => that.showArticleList(data))
          // eslint-disable-next-line no-console
          .catch(err => console.error(err));
      },
      renderItem: function(item, search) {
        let s = search.replace(/[-/\\^$*+?.()|[\]{}]/g, "\\$&"),
          re = new RegExp("(" + s.split(" ").join("|") + ")", "gi");
        return "<div class=\"autocomplete-suggestion\" data-id=\"" + item.id + "\" data-val=\"" + item.title + "\">" + item.title.replace(re, "<b>$1</b>") + "</div>";
      },
    });
  }

  ///////////////////////////////////////////////////////////
  // functions to fetch data from db

  _fetchArticles() {
    this._getData("search")
      .then(data => {
        this.allArticles = data;
        this.searchChoices = data;
      })
      // eslint-disable-next-line no-console
      .catch(err => console.error(err));
  }

  async _getData(url = "") {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error("BadResponseCode: " + response.status.toString());
    }
    return await response.json();
  }

  ///////////////////////////////////////////////////////////
  // helper functions

  createEvent(type, data, msg) {
    let event = new Event(type);
    if (data !== null && data !== undefined) {
      event.data = data;
    }
    if (msg !== null && msg !== undefined) {
      event.msg = msg;
    }
    return event;
  }
}

export default new ArticleSidebar();
