/* global autoComplete */

import config from "./config.js";

class ArticleSidebar {
    constructor() {
        // this.fetchSearchChoices();
        this.initSearchAutocomplete();
    }

    initSearchAutocomplete() {
        return new autoComplete({
            selector: "#search",
            minChars: 2,
            source: function (term, suggest) {
                fetch(window.location.href + "search/" + term)
                    .then(response => {
                        if (response.status !== 200) {
                            throw new Error("BadResponseCode: " + response.status.toString());
                        }
                        return response.json();
                    })
                    .then(data => {
                        suggest(data);
                    })
                    .catch(err => {
                        // eslint-disable-next-line no-console
                        console.error(err);
                    });
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

    // initSearchAutocomplete(choices) {
    //     return new autoComplete({
    //         selector: "#search",
    //         minChars: 2,
    //         source: function (term, suggest) {
    //             let re = RegExp(term.toLowerCase(), "gi");
    //             suggest(choices.filter(item => re.test(item)));
    //         },
    //         onSelect(event, term, item) {
    //             // TODO: cklick action
    //         },
    //     });
    // }

    fetchSearchChoices() {
        fetch(window.location.href + "search")
            .then(response => {
                if (response.status !== 200) {
                    throw new Error("BadResponseCode: " + response.status.toString());
                }
                return response.json();
            })
            .then(data => {
                this.initSearchAutocomplete(data);
            })
            .catch(err => {
                // eslint-disable-next-line no-console
                console.error(err);
            });
    }
}

export default new ArticleSidebar();