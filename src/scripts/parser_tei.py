import xml.etree.ElementTree as ET

_namespace = {"dhd": "http://www.tei-c.org/ns/1.0", "xml": "http://www.w3.org/XML/1998/namespace"}
_dictOrg = {}
_dictLocation = {}

def parse(path):
    tree = ET.parse(path)

    # nodeTitleStmt = tree.find(".//dhd:titleStmt", _namespace)
    # title = nodeTitleStmt.findall("./dhd:title", _namespace)

    print(path)
    #find categoty/subcategory
    nodeProfileDesc = tree.find(".//dhd:profileDesc", _namespace)
    for element in nodeProfileDesc.findall(".//dhd:textClass/dhd:keywords", _namespace):
        if (element.attrib["n"]) != "category":
            print(element.attrib["n"] + ": ", end="")
            for term in element.findall("./dhd:term", _namespace):
                print(term.text, end=", ")
            print()

    print("\n")