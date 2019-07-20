/* eslint-disable no-magic-numbers */

class Config {
    constructor() {
        /* COLORS */
        this.COUNTRY_BORDERS = "#FFF";
        this.COUNTRIES = "#75ACAE";
        this.MARKER_LOCATION = "#BC5B65";
        this.PEOPLE_AT_LOCATION = "#4D5555";
        this.NETWORK_LINES = "#1D3641";
        this.HIGHLIGHT = "#ffba49";
        this.ACTIVE = "#ba1b1d";

        /* MAP */
        this.SCALE = 1600;
        this.CENTER = [10, 50];

        /* FETCHING */
        this.RESPONSE_SUCCESS = 200;

        /* VISUALIZATION */
        this.NOT_PARTICIPATING_OPACITY = 0.5;
        this.PEOPLE_AT_LOCATION_OPACITY = 0.6;
        this.MARKER_LOCATION_RADIUS = 3.5;
        this.NETWORK_LINES_OPACITY = 0.3;
        this.NETWORK_LINES_STROKE_WIDTH = 2;
    }
}

export default new Config();
