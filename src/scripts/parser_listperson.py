import xml.etree.ElementTree as ET

namespace = {"dhd": "http://www.tei-c.org/ns/1.0", "xml": "http://www.w3.org/XML/1998/namespace"}

def parse(path):
    dictPerson = {}

    tree = ET.parse(path)
    nodeListPerson = tree.find(".//dhd:listPerson", namespace)

    people = nodeListPerson.findall("dhd:person", namespace)
    
    for nodePerson in people:
        person = parsePerson(nodePerson)
        dictPerson[person["id"]] = person

    return dictPerson

def parsePerson(nodePerson):
    id = nodePerson.attrib["{%s}id" % namespace["xml"]]

    orga = None
    nodeOrga = nodePerson.find("./dhd:affiliation[@ref]", namespace)
    if nodeOrga is not None:
        orga = nodeOrga.attrib["ref"][1:] # remove hashtag on ref string
        
    return {
        "id": id,
        "firstName": nodePerson.find("./dhd:persName/dhd:forename", namespace).text,
        "lastName": nodePerson.find("./dhd:persName/dhd:surname", namespace).text,
        "orga": orga
    }