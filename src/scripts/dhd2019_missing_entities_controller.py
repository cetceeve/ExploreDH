import json
import novatim_adapter as geocoder

def __writeMissingEntityInfoFile(dictPerson, dictOrga):
    file = open("dhd2019_missing_info.txt", mode="w", encoding="utf-8")

    file.write("Personen ohne Organisation:")
    # get people with no associated organisation
    for person in dictPerson.values():
        if "__temp__affil" in person:
            file.write("\n" + json.dumps(person, indent=4, ensure_ascii=False))
    
    file.write("\n\nLocations ohne Koordinaten:")
    # get orgas with no location
    for orga in dictOrga.values():
        if "location" not in orga:
            file.write("\n" + json.dumps(orga, indent=4, ensure_ascii=False))

    file.close()


def __writeAdditionalEntityJSONFile(dictPerson, dictOrga):
    with open("dhd2019_missing_entities.json", mode="w", encoding="utf-8") as file:
        NEW_ORGAS_ID_BASE = 1000
        peopleMissingOrgas = []
        additionalOrgas = []
        orgasMissingLocations = []
        missingPeople = []
        res = {
            "peopleMissingOrgas": peopleMissingOrgas,
            "additionalOrgas": additionalOrgas,
            "orgasMissingLocations": orgasMissingLocations,
            "missingPeople": missingPeople
        }

        # get people with no associated organisation
        counter = NEW_ORGAS_ID_BASE # start org ids high to not conflict with existing ones
        for person in dictPerson.values():
            if "__temp__affil" in person:
                person["orga"] = "org__" + str(counter)
                peopleMissingOrgas.append(person)
                counter += 1

        # create new organisations for the people missing it
        for i in range(counter - NEW_ORGAS_ID_BASE):
            additionalOrgas.append({
                "id": "org__" + str(NEW_ORGAS_ID_BASE + i),
                "name": "{{enter useful organisation name e.g. Germanisches Nationalmuseum, Nürnberg }}",
                "loc_query": "{{enter city, country here (will be processed by novatim) z.B. Nürnberg, Deutschland}}"
            })

        # get orgas with no location
        for orga in dictOrga.values():
            if "location" not in orga:
                orgasMissingLocations.append({
                    "id": orga["id"],
                    "name": orga["name"],
                    "loc_query": "{{enter city name here (will be processed by novatim)  z.B. Würzburg, Deutschland}}"
                })
        
        file.write(json.dumps(res, indent=4, ensure_ascii=False))


def getAdditionalEntities(dictPerson, dictOrga, dictLocation):
    with open("dhd2019_missing_entities.json", mode="r", encoding="utf-8") as file:
        data = json.load(file)

        peopleMissingOrgas = data["peopleMissingOrgas"]
        additionalOrgas = data["additionalOrgas"]
        orgasMissingLocations = data["orgasMissingLocations"]

        for person in peopleMissingOrgas:
            del person["__temp__affil"]
            dictPerson[person["id"]] = person

        for orga in additionalOrgas:
            dictOrga[orga["id"]] = _resolveLocationQuery(orga, dictLocation)

        for orga in orgasMissingLocations:
            dictOrga[orga["id"]] = _resolveLocationQuery(orga, dictLocation)


def _resolveLocationQuery(orga, dictLocation):
    geoData = geocoder.getLocation(orga["loc_query"])
    locId = _getLocationId(orga["loc_query"], geoData , dictLocation)

    orga["location"] = locId
    del orga["loc_query"]
    return orga


def _getLocationId(query, geoData, dictLocation):
    cityName = query.split(",")[0] # loc_query was "city, country"

    # check for already existing locations
    for loc in dictLocation.values():
        if loc["name"] == cityName and loc["lat"][:2] == geoData["lat"][:2] and loc["lon"][:2] == geoData["lon"][:2]:
            return loc["id"]

    locID = str(geoData["raw"]["place_id"])
    dictLocation[locID] = {
        "id": locID,
        "name": cityName,
        "lat": geoData["lat"],
        "lon": geoData["lon"]
    }
    return locID


def fixTimGeelhaar(dictPerson):
    dictPerson["person__geelhaar-em-uni-frankfurt-de"]["orga"] = "org__47"

    # original:
    # "person__geelhaar-em-uni-frankfurt-de": {
    #   "id": "person__geelhaar-em-uni-frankfurt-de", 
    #   "firstName": "Tim", 
    #   "lastName": "Geelhaar", 
    #   "orga": "org_47"}
    # 

def addWalterScholger(dictPerson):
    dictPerson["person__walter-scholger-uni-graz-at"] = {
        "id": "person__walter-scholger-uni-graz-at",
        "firstName": "Walter",
        "lastName": "Scholger",
        "orga": "org__74"
    }
