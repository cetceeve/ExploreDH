import xml.etree.ElementTree as ET

_namespace = {"dhd": "http://www.tei-c.org/ns/1.0", "xml": "http://www.w3.org/XML/1998/namespace"}
_dictOrg = {}
_dictLocation = {}

def parse(path):
    tree = ET.parse(path)

    # Panels cannot be taken into account
    if tree.find(".//dhd:profileDesc/dhd:textClass/dhd:keywords[@n='subcategory']/dhd:term", _namespace).text == "Panel":
        return None

    return tree
                
    # print(path)
    # #find categoty/subcategory
    # nodeProfileDesc = tree.find(".//dhd:profileDesc", _namespace)
    # for element in nodeProfileDesc.findall(".//dhd:textClass/dhd:keywords", _namespace):
    #     if (element.attrib["n"]) != "category":
    #         print(element.attrib["n"] + ": ", end="")
    #         for term in element.findall("./dhd:term", _namespace):
    #             print(term.text, end=", ")
    #         print()

    # print("\n")

def getEmails(tree, dictPerson):
    nodeTitleStmt = tree.find(".//dhd:titleStmt", _namespace)

    for person in nodeTitleStmt.findall("./dhd:author", _namespace):
        personId = _redirectWrongIds(person.get("ref")[1:]) # remove hashtag from ref
        
        if "email" not in dictPerson[personId]:
            dictPerson[personId]["email"] = [person.find("./dhd:email", _namespace).text]
        elif person.find("./dhd:email", _namespace).text not in dictPerson[personId]["email"]:
            dictPerson[personId]["email"].append(person.find("./dhd:email", _namespace).text)

def getTitle(tree, dictArticle):
    nodeTitle = tree.find(".//dhd:titleStmt/dhd:title[@type='full']", _namespace)

    if nodeTitle is not None:
        fullTitle = nodeTitle.find("./dhd:title[@type='main']", _namespace).text
        subTitle = nodeTitle.find("./dhd:title[@type='sub']", _namespace).text
        if subTitle is not None:
            fullTitle += ": " + subTitle
        return fullTitle
    else:
        return tree.find(".//dhd:titleStmt/dhd:title", _namespace).text


def _redirectWrongIds(personId):
    if personId == "person__tobias-hodel-hist-uzh-ch":
        return "person__tobias-hodel-uzh-ch"
    elif personId == "person__diem-caa-tuwien-ac-at":
        return "person__diem-cvl-tuwien-ac-at"
    elif personId == "person__leonardkonle-gmail-com":
        return "person__leonard-konle-uni-wuerzburg-de"
    elif personId == "person__frank-puppe-informatik-uni-wuerzburg-de":
        return "person__frank-puppe-uni-wuerzburg-de"
    elif personId == "person__schnoepf-bbaw-de":
        return "person__schnoepf-i-d-e-de"
    elif personId == "person__f-rau-uni-koeln-de":
        return "person__frau-uni-koeln-de"
    elif personId == "person__markus-krug-uni-wuerzburg-de":
        return "person__markus-krug-informatik-uni-wuerzburg-de"
    
    return personId