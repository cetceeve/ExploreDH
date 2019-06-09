import xml.etree.ElementTree as ET
import re

from constants import NAMESPACE_XML

def parse(path, dictOrga, dictLocation):
    tree = ET.parse(path)

    nodeListPerson = tree.find(".//dhd:listOrg", NAMESPACE_XML)
    nodeOrgas = nodeListPerson.findall("./dhd:org", NAMESPACE_XML)
    
    for nodeOrga in nodeOrgas:
        orga = _parseOrga(nodeOrga, dictLocation)
        dictOrga[orga["id"]] = orga


def _parseOrga(nodeOrga, dictLocation):
    orga =  {
        "id": nodeOrga.get("{{{}}}id".format(NAMESPACE_XML["xml"])),
        "name": re.sub(r"\n\s*", " " , nodeOrga.find("./dhd:orgName", NAMESPACE_XML).text) # regex for newlines with trailing spaces
    }

    # deal with orgas having no location
    nodeLocation = nodeOrga.find("./dhd:location", NAMESPACE_XML)
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
        "id": nodeLocation.find("./dhd:placeName", NAMESPACE_XML).get("key")[21:], # remove link
        "name": re.sub(r"\n\s*", " " , nodeLocation.find("./dhd:placeName", NAMESPACE_XML).text), # regex for newlines with trailing spaces
        "lat": nodeLocation.find("./dhd:geo", NAMESPACE_XML).text.split(" ")[1],
        "lon": nodeLocation.find("./dhd:geo", NAMESPACE_XML).text.split(" ")[0]
    }
    return location
    


        