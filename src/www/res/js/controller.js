import sidebar from "./article_sidebar.js";
import map from "./map_d3.js";

class Controller {
    constructor() {
        this.addSidebarEventListeners();
        this.addMapEventListeners();
    }

    addSidebarEventListeners() {
        return;
    }

    addMapEventListeners() {
        map.addEventListener("onMarkerClicked", event => {
            sidebar.setArticlesByOrga(event.data);
        });
        return;
    }

}

export default new Controller();