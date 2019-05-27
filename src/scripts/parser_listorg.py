import xml.etree.ElementTree as ET
import re

namespace = {"dhd": "http://www.tei-c.org/ns/1.0", "xml": "http://www.w3.org/XML/1998/namespace"}

def parse(path):
    dictOrg = {}
    dictLocation = {}

    tree = ET.parse(path)

    nodeListPerson = tree.find(".//dhd:listOrg", namespace)
    orgas = nodeListPerson.findall("./dhd:org", namespace)
    
    for nodeOrga in orgas:
        orga = parseOrga(nodeOrga, dictLocation)
        dictOrg[orga["id"]] = orga

    return (dictOrg, dictLocation)

def parseOrga(nodeOrga, dictLocation):
    orga =  {
        "id": nodeOrga.attrib["{%s}id" % namespace["xml"]],
        "name": re.sub("\n\s*", " " , nodeOrga.find("./dhd:orgName", namespace).text)
    }

    nodeLocation = nodeOrga.find("./dhd:location", namespace)
    if nodeLocation is not None:
        location = parseLocation(nodeLocation)
        orga["location"] = location["id"]
        
        if location["id"] not in dictLocation:
            dictLocation[location["id"]] = location
            
    return orga

def parseLocation(nodeLocation):
    location = {
        "id": nodeLocation.find("./dhd:placeName", namespace).attrib["key"][21:], # remove link
        "name": re.sub("\n\s*", " " , nodeLocation.find("./dhd:placeName", namespace).text),
        "lat": nodeLocation.find("./dhd:geo", namespace).text.split(" ")[0],
        "lon": nodeLocation.find("./dhd:geo", namespace).text.split(" ")[1]
    }

    return location
    


        