/* global autoComplete */

class ArticleSidebar extends EventTarget {
    constructor() {
        super();
        // initial state
        this.allArticleTitles = [];
        this.searchChoices = [];
        this._initSearchAutocomplete(this);

        // set all articles as seatch choices
        this._fetchArticleTitles();
        this.setArticlesByOrga("org__128");
    }

    setSearchChoices(_choices) {
        if (!(_choices !== undefined && _choices !== null && _choices.length !== 0)) {
            this.searchChoices = this.allArticleTitles;
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
                suggest(that.searchChoices.filter(item => re.test(item.toLowerCase())));
            },
            onSelect(event, term) {
                fetch(window.location.href + "article/" + term)
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
        });
    }

    _fetchArticleTitles() {
        fetch(window.location.href + "search")
            .then(response => {
                if (response.status !== 200) {
                    throw new Error("BadResponseCode: " + response.status.toString());
                }
                return response.json();
            })
            .then(data => {
                this.allArticleTitles = data;
                this.searchChoices = data;
            })
            .catch(err => {
                // eslint-disable-next-line no-console
                console.error(err);
            });
    }
}

export default new ArticleSidebar();