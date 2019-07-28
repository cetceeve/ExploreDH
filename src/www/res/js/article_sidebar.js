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
            "<li>" +
            "<div class='uk-card uk-card-default uk-card-body uk-card-hover'>" +
            "<h3 class='uk-card-title cardHead'><%=title%></h3>" +
            "<p><%=authors.join(', ')%></p>" +
            "<div class='uk-card-footer keywords'>" +
            "<% for (let keyword in keywords) { %>" +
            "<span class='uk-badge'><%=keywords[keyword]%></span>" +
            "<% } %>" +
            "</div>" +
            "</div>" +
            "</li>"
        );
    }

    //////////////////////////////////////////////////////
    // functions for controller

  clearArticleListAndSearchChoices() {
    while (this.articleListEl.firstChild) {
      this.articleListEl.removeChild(this.articleListEl.firstChild);
    }

    setLocationName(name) {
        let locationNameEl = document.querySelector("#locationName");

        this.locationContainerEl.style.visibility = "visible";
        locationNameEl.innerHTML = name;
        this.clearLocationButton.addEventListener("click", () => this.clearLocationName());
    }

    //////////////////////////////////////////////////////

    showArticleList(articleList) {
        this.clearArticleListAndSearchChoices();

        for (let entry of articleList) {
            let container = document.createElement("div"),
                articleHTML = this.articleTemplate(entry);

            container.innerHTML = articleHTML;
            container.id = entry.id;
            this.articleListEl.appendChild(container);
        }
    }

    setSearchChoices(_choices) {
        if (!(_choices !== undefined && _choices !== null && _choices.length !== 0)) {
            this.searchChoices = this.allArticles;
        } else {
            this.searchChoices = _choices;
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
        this.clearArticleListAndSearchChoices();
        super.dispatchEvent(this.createEvent("onLocationReset", this.currentOrgaId));
    }

    _initSearchAutocomplete(that) {
        return new autoComplete({
            selector: "#search",
            minChars: 2,
            cache: false,
            source: function (term, suggest) {
                let re = RegExp(term.toLowerCase(), "gi");
                suggest(that.searchChoices.filter(item => re.test(item.title.toLowerCase())));
            },
            onSelect(event, term, item) {
                that._getData("article/" + item.dataset.id)
                    .then(data => that.showArticleList(data))
                    // eslint-disable-next-line no-console
                    .catch(err => console.error(err));
            },
            renderItem: function (item, search) {
                let s = search.replace(/[-/\\^$*+?.()|[\]{}]/g, "\\$&"),
                    re = new RegExp("(" + s.split(" ").join("|") + ")", "gi");
                return "<div class=\"autocomplete-suggestion\" data-id=\"" + item.id + "\" data-val=\"" + item.title + "\">" + item.title.replace(re, "<b>$1</b>") + "</div>";
            },
        });
    }

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

    //////////////////////////////////////////////////////
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
    return await response.json();
  }
}

export default new ArticleSidebar();
