import requests
import json # for developement only

queryBaseString = "https://nominatim.openstreetmap.org/search"
payload = {"q": "Eden, Loonaverse", "format": "json", "addressdetails": "1", "limit": 1}

def getLocation(query):
    payload["q"] = query
    r = requests.get(queryBaseString, params=payload)
    

    # pylint: disable=no-member
    if r.status_code == requests.codes.ok:
        # prettyprint json
        # print(json.dumps(r.json(), indent=4, sort_keys=True))
        data = r.json()
        return {
            "lat": data[0]["lat"],
            "lon": data[0]["lon"],
            "type": data[0]["type"],
            "raw": data[0]
        }
    else:
        return None