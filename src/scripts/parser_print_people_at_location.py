import json
import parsercache as cache

def printPeopleAtLocation(dictPerson, dictOrga, dictLocation):
    dictRes = {}
    # deepcopy dictLocation with new params
    for loc in dictLocation.values():
        dictRes[loc["id"]] = {
            "id": loc["id"],
            "lat": loc["lat"],
            "lon": loc["lon"],
            "numOfPeople": 0
        }

    # count people per location
    for person in dictPerson.values():
        dictRes[dictOrga[person["orga"]]["location"]]["numOfPeople"] += 1
        
        # in long form:
        # orga = dictOrga[person["orga"]]     
        # location = orga["location"]
        # resEntry = dictRes["location"]
        # resEntry["numOfPeople"] += 1

    # convert to array
    resArray = []
    for datapoint in dictRes.values():
        del datapoint["id"]
        resArray.append(datapoint)
    
    # print(json.dumps(resArray, indent=4, ensure_ascii=False))
    cache.write(resArray, "peopleAtLocation")