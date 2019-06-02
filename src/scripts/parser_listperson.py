import xml.etree.ElementTree as ET

from constants import NAMESPACE_XML

def parse(path, dictPerson):
    tree = ET.parse(path)
    
    nodeListPerson = tree.find(".//dhd:listPerson", NAMESPACE_XML)
    people = nodeListPerson.findall("./dhd:person", NAMESPACE_XML)
    
    for nodePerson in people:
        person = _parsePerson(nodePerson)
        dictPerson[person["id"]] = person

def _parsePerson(nodePerson):
    person =  {
        "id": nodePerson.attrib["{%s}id" % NAMESPACE_XML["xml"]],
        "firstName": nodePerson.find("./dhd:persName/dhd:forename", NAMESPACE_XML).text,
        "lastName": nodePerson.find("./dhd:persName/dhd:surname", NAMESPACE_XML).text,
    }

    # deal with people having no ref to any organisation
    nodeOrga = nodePerson.find("./dhd:affiliation[@ref]", NAMESPACE_XML)
    if nodeOrga is not None:
        person["orga"] = nodeOrga.attrib["ref"][1:] # remove hashtag on ref string
    else:
        person["__temp__affil"] = nodePerson.find("./dhd:affiliation", NAMESPACE_XML).text
    
    return person
        