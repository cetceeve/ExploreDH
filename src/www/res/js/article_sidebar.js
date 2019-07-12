/* global autoComplete */

import config from "./config.js";

class ArticleSidebar {
    constructor() {
        this.articleTitles = [];
        this.fetchArticleTitles();
        this.initSearchAutocomplete(this);
    }

    setSearchChoices(_choices) {
        if (!(_choices !== undefined && _choices !== null && _choices.length !== 0)) {
            this.choices = this.articleTitles;
        } else {
            this.choices = _choices;
        }
    }

    // initSearchAutocomplete() {
    //     return new autoComplete({
    //         selector: "#search",
    //         minChars: 2,
    //         source: function (term, suggest) {
    //             fetch(window.location.href + "search/" + term)
    //                 .then(response => {
    //                     if (response.status !== 200) {
    //                         throw new Error("BadResponseCode: " + response.status.toString());
    //                     }
    //                     return response.json();
    //                 })
    //                 .then(data => {
    //                     suggest(data);
    //                 })
    //                 .catch(err => {
    //                     // eslint-disable-next-line no-console
    //                     console.error(err);
    //                 });
    //         },
    //         onSelect(event, term) {
    //             fetch(window.location.href + "article/" + term)
    //                 .then(response => {
    //                     if (response.status !== 200) {
    //                         throw new Error("BadResponseCode: " + response.status.toString());
    //                     }
    //                     return response.json();
    //                 })
    //                 .then(data => {
    //                     console.log(data);
    //                 })
    //                 .catch(err => {
    //                     // eslint-disable-next-line no-console
    //                     console.error(err);
    //                 });
    //         },
    //     });
    // }

    initSearchAutocomplete(that) {
        return new autoComplete({
            selector: "#search",
            minChars: 2,
            source: function (term, suggest) {
                let re = RegExp(term.toLowerCase(), "gi");
                suggest(that.choices.filter(item => re.test(item)));
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

    fetchArticleTitles() {
        fetch(window.location.href + "search")
            .then(response => {
                if (response.status !== 200) {
                    throw new Error("BadResponseCode: " + response.status.toString());
                }
                return response.json();
            })
            .then(data => {
                this.articleTitles = data;
                this.setSearchChoices();
            })
            .catch(err => {
                // eslint-disable-next-line no-console
                console.error(err);
            });
    }
}

export default new ArticleSidebar();