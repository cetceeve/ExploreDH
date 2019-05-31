import json
import parser_io as io

def printPeopleAtLocation(dictPerson, dictOrga, dictLocation):
    dictRes = {}
    # deepcopy dictLocation with new params
    for loc in dictLocation.values():
        dictRes[loc["id"]] = {
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

    io.write(io.source["output"], list(dictRes.values()), "peopleAtLocation")