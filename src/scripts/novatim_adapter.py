import requests
import json

_queryBaseString = "https://nominatim.openstreetmap.org/search"
_payload = {"q": "Eden, Loonaverse", "format": "json", "addressdetails": "1", "limit": 1}

def getLocation(query):
    _payload["q"] = query
    r = requests.get(_queryBaseString, params=_payload)
    print("Geocoder, searching for: " + query)

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
    else:
        return None