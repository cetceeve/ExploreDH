/* global autoComplete */

class ArticleSidebar extends EventTarget {
    constructor() {
        super();
        // initial state
        this.allArticles = [];
        this.searchChoices = [];
        this._initSearchAutocomplete(this);

        // set all articles as search choices
        this._fetchArticles();
        this.setArticlesByOrga("org__121");
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
            .then(data => console.log(data))
            // eslint-disable-next-line no-console
            .catch(err => console.error(err));
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
                    .then(data => console.log(data))
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