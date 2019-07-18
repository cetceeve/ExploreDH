/* global autoComplete _ */

class ArticleSidebar extends EventTarget {
    constructor() {
        super();
        // initial state
        this.allArticles = [];
        this.searchChoices = [];
        this._initSearchAutocomplete(this);

        // set all articles as search choices
        this._fetchArticles();
        //  this.setArticlesByOrga("org__121");

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

    setSearchChoices(_choices) {
        if (!(_choices !== undefined && _choices !== null && _choices.length !== 0)) {
            this.searchChoices = this.allArticles;
        } else {
            this.searchChoices = _choices;
        }
    }

    setArticlesByOrga(orgaID) {
        this._getData("article/articleByOrga/" + orgaID)
            .then(data => this.showArticles(data))
            // eslint-disable-next-line no-console
            .catch(err => console.error(err));
    }

    showArticles(articleList) {
        let articleListEl = document.querySelector("#articleList");
        while (articleListEl.firstChild) {
            articleListEl.removeChild(articleListEl.firstChild);
        }

        for (let entry of articleList) {
            this.showArticle(articleListEl, entry);
        }
    }

    showArticle(articleListEl, article) {
        if (articleListEl === null) {
            // eslint-disable-next-line no-param-reassign
            articleListEl = document.querySelector("#articleList");
        }

        let container = document.createElement("div"),
            articleHTML = this.articleTemplate(article);

        container.innerHTML = articleHTML;
        container.id = article.id;
        articleListEl.appendChild(container);
    }

    _initSearchAutocomplete(that) {
        return new autoComplete({
            selector: "#search",
            minChars: 2,
            source: function (term, suggest) {
                let re = RegExp(term.toLowerCase(), "gi");
                suggest(that.searchChoices.filter(item => re.test(item.title.toLowerCase())));
            },
            onSelect(event, term, item) {
                that._getData("article/" + item.dataset.id)
                    .then(data => that.showArticle(null, data))
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
}

export default new ArticleSidebar();