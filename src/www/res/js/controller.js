import sidebar from "./article_sidebar.js";
import map from "./map_d3.js";

class Controller {
    constructor() {
        this.addSidebarEventListeners();
        this.addMapEventListeners();
    }

    addSidebarEventListeners() {
        sidebar.addEventListener("onLocationReset", event => {
            map.resetLocation(event.data);
        });
    }

    addMapEventListeners() {
        map.addEventListener("onMarkerClicked", event => {
            sidebar.setArticlesByOrga(event.data.id);
            sidebar.setLocationName(event.data.name);
        });
    }

}

export default new Controller();