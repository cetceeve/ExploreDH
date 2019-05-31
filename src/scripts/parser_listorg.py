import xml.etree.ElementTree as ET
import re

from constants import NAMESPACE

def parse(path, dictOrga, dictLocation):
    tree = ET.parse(path)

    nodeListPerson = tree.find(".//dhd:listOrg", NAMESPACE)
    orgas = nodeListPerson.findall("./dhd:org", NAMESPACE)
    
    for nodeOrga in orgas:
        orga = _parseOrga(nodeOrga, dictLocation)
        dictOrga[orga["id"]] = orga


def _parseOrga(nodeOrga, dictLocation):
    orga =  {
        "id": nodeOrga.attrib["{%s}id" % NAMESPACE["xml"]],
        "name": re.sub(r"\n\s*", " " , nodeOrga.find("./dhd:orgName", NAMESPACE).text) # regex for newlines with trailing spaces
    }

    # deal with orgas having no location
    nodeLocation = nodeOrga.find("./dhd:location", NAMESPACE)
    if nodeLocation is not None:
        location = _parseLocation(nodeLocation)
        orga["location"] = location["id"]
        
        _addToDictLocation(location, dictLocation)
    return orga


def _addToDictLocation(location, dictLocation):
    if location["id"] not in dictLocation:
            dictLocation[location["id"]] = location


def _parseLocation(nodeLocation):
    location = {
        "id": nodeLocation.find("./dhd:placeName", NAMESPACE).attrib["key"][21:], # remove link
        "name": re.sub(r"\n\s*", " " , nodeLocation.find("./dhd:placeName", NAMESPACE).text), # regex for newlines with trailing spaces
        "lat": nodeLocation.find("./dhd:geo", NAMESPACE).text.split(" ")[1],
        "lon": nodeLocation.find("./dhd:geo", NAMESPACE).text.split(" ")[0]
    }
    return location
    


        