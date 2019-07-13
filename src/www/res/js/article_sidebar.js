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
    }

    setSearchChoices(_choices) {
        if (!(_choices !== undefined && _choices !== null && _choices.length !== 0)) {
            this.searchChoices = this.allArticles;
        } else {
            this.searchChoices = _choices;
        }
    }

    setArticlesByOrga(orgaID) {
        fetch(window.location.href + "article/articleByOrga/" + orgaID)
            .then(response => {
                if (response.status !== 200) {
                    throw new Error("BadResponseCode: " + response.status.toString());
                }
                return response.json();
            })
            .then(data => {
                console.log(data);
            })
            .catch(err => {
                // eslint-disable-next-line no-console
                console.error(err);
            });
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
                fetch(window.location.href + "article/" + item.dataset.id)
                    .then(response => {
                        if (response.status !== 200) {
                            throw new Error("BadResponseCode: " + response.status.toString());
                        }
                        return response.json();
                    })
                    .then(data => {
                        console.log(data);
                    })
                    .catch(err => {
                        // eslint-disable-next-line no-console
                        console.error(err);
                    });
            },
            renderItem: function (item, search) {
                let s = search.replace(/[-/\\^$*+?.()|[\]{}]/g, "\\$&"),
                    re = new RegExp("(" + s.split(" ").join("|") + ")", "gi");
                return "<div class=\"autocomplete-suggestion\" data-id=\"" + item.id + "\" data-val=\"" + item.title + "\">" + item.title.replace(re, "<b>$1</b>") + "</div>";
            },
        });
    }

    _fetchArticles() {
        fetch(window.location.href + "search")
            .then(response => {
                if (response.status !== 200) {
                    throw new Error("BadResponseCode: " + response.status.toString());
                }
                return response.json();
            })
            .then(data => {
                this.allArticles = data;
                this.searchChoices = data;
            })
            .catch(err => {
                // eslint-disable-next-line no-console
                console.error(err);
            });
    }
}

export default new ArticleSidebar();