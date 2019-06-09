import requests
import json

from constants import NOVATIM_SEARCH_URL

def getLocation(query):
    print("Geocoder, searching for: " + query)
    r = requests.get(NOVATIM_SEARCH_URL, params={"q": query, "format": "json", "addressdetails": "1", "limit": 1})

    # pylint: disable=no-member
    if r.status_code == requests.codes.ok:
        data = r.json()
        if data:
            return {
                "lat": data[0]["lat"],
                "lon": data[0]["lon"],
                "type": data[0]["type"],
                "raw": data[0]
            }
    
    return None