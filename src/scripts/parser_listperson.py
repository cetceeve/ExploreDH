import xml.etree.ElementTree as ET

_namespace = {"dhd": "http://www.tei-c.org/ns/1.0", "xml": "http://www.w3.org/XML/1998/namespace"}
_dictPerson = {}

def parse(path):
    tree = ET.parse(path)
    
    nodeListPerson = tree.find(".//dhd:listPerson", _namespace)
    people = nodeListPerson.findall("./dhd:person", _namespace)
    
    for nodePerson in people:
        person = _parsePerson(nodePerson)
        _dictPerson[person["id"]] = person

    return _dictPerson

def _parsePerson(nodePerson):
    person =  {
        "id": nodePerson.attrib["{%s}id" % _namespace["xml"]],
        "firstName": nodePerson.find("./dhd:persName/dhd:forename", _namespace).text,
        "lastName": nodePerson.find("./dhd:persName/dhd:surname", _namespace).text,
    }

    # deal with people having no ref to any organisation
    nodeOrga = nodePerson.find("./dhd:affiliation[@ref]", _namespace)
    if nodeOrga is not None:
        person["orga"] = nodeOrga.attrib["ref"][1:] # remove hashtag on ref string
    else:
        person["__temp__affil"] = nodePerson.find("./dhd:affiliation", _namespace).text
    
    return person
        