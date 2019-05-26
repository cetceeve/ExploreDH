import xml.etree.ElementTree as ET

def readListPerson(path):
    namespace = {"dhd": "http://www.tei-c.org/ns/1.0"}

    tree = ET.parse(path)
    nodeListPerson = tree.find(".//dhd:listPerson", namespace)

    people = nodeListPerson.findall("dhd:person", namespace)
    print(len(people))