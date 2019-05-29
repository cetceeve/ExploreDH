import xml.etree.ElementTree as ET
import re

_namespace = {"dhd": "http://www.tei-c.org/ns/1.0", "xml": "http://www.w3.org/XML/1998/namespace"}
_dictOrg = {}
_dictLocation = {}

def parse(path):
    tree = ET.parse(path)

    nodeListPerson = tree.find(".//dhd:listOrg", _namespace)
    orgas = nodeListPerson.findall("./dhd:org", _namespace)
    
    for nodeOrga in orgas:
        orga = _parseOrga(nodeOrga)
        _dictOrg[orga["id"]] = orga

    return (_dictOrg, _dictLocation)


def _parseOrga(nodeOrga):
    orga =  {
        "id": nodeOrga.attrib["{%s}id" % _namespace["xml"]],
        "name": re.sub(r"\n\s*", " " , nodeOrga.find("./dhd:orgName", _namespace).text)
    }

    # deal with orgas having no location
    nodeLocation = nodeOrga.find("./dhd:location", _namespace)
    if nodeLocation is not None:
        location = _parseLocation(nodeLocation)
        orga["location"] = location["id"]
        
        _addToDictLocation(location)
    return orga


def _addToDictLocation(location):
    if location["id"] not in _dictLocation:
            _dictLocation[location["id"]] = location


def _parseLocation(nodeLocation):
    location = {
        "id": nodeLocation.find("./dhd:placeName", _namespace).attrib["key"][21:], # remove link
        "name": re.sub(r"\n\s*", " " , nodeLocation.find("./dhd:placeName", _namespace).text),
        "lat": nodeLocation.find("./dhd:geo", _namespace).text.split(" ")[1], # lat
        "lon": nodeLocation.find("./dhd:geo", _namespace).text.split(" ")[0]  # lon
    }
    return location
    


        