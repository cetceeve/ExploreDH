import xml.etree.ElementTree as ET
import uuid

from constants import NAMESPACE_XML, PERSON_ID_LOOKUP_DICT


def parse(path, dictPerson, dictArticle, dictKeyword):
    tree = ET.parse(path)

    # Panels cannot be taken into account
    if tree.find(".//dhd:profileDesc/dhd:textClass/dhd:keywords[@n='subcategory']/dhd:term", NAMESPACE_XML).text != "Panel":
        _getEmails(tree, dictPerson)
        _getArticle(tree, dictArticle, dictKeyword)


def _getEmails(tree, dictPerson):
    nodeTitleStmt = tree.find(".//dhd:titleStmt", NAMESPACE_XML)

    for person in nodeTitleStmt.findall("./dhd:author", NAMESPACE_XML):
        personId = _redirectWrongIds(person.get("ref")[1:])  # remove hashtag from ref

        # check if person has an email already, append if necessary
        if "email" not in dictPerson[personId]:
            dictPerson[personId]["email"] = [person.find("./dhd:email", NAMESPACE_XML).text]
        elif person.find("./dhd:email", NAMESPACE_XML).text not in dictPerson[personId]["email"]:
            dictPerson[personId]["email"].append(person.find("./dhd:email", NAMESPACE_XML).text)


def _getArticle(tree, dictArticle, dictKeyword):
    articleID = str(uuid.uuid1())

    dictArticle[articleID] = {
        "id": articleID,
        "title": _getTitle(tree),
        "abstract": "ASSA!",
        "keywords": _getKeywords(tree, dictKeyword),
        "authors": _getAuthors(tree)
    }


def _getTitle(tree):
    nodeTitle = tree.find(".//dhd:titleStmt/dhd:title[@type='full']", NAMESPACE_XML)

    if nodeTitle is not None:
        fullTitle = nodeTitle.find("./dhd:title[@type='main']", NAMESPACE_XML).text
        subTitle = nodeTitle.find("./dhd:title[@type='sub']", NAMESPACE_XML).text
        if subTitle is not None:
            fullTitle += ": " + subTitle
        return fullTitle
    else:
        return tree.find(".//dhd:titleStmt/dhd:title", NAMESPACE_XML).text


def _getKeywords(tree, dictKeyword):
    keywords = []
    # find keywords
    nodeProfileDesc = tree.find(".//dhd:profileDesc", NAMESPACE_XML)
    for element in nodeProfileDesc.findall(".//dhd:textClass/dhd:keywords", NAMESPACE_XML):
        if element.attrib["n"] == "keywords":
            terms = [term.text for term in element.findall("./dhd:term", NAMESPACE_XML)]

    for term in list(dict.fromkeys(terms)):  # remove duplicates
        keywords.append(_getKeywordIdByName(dictKeyword, term))
    return keywords


def _getAuthors(tree):
    nodeTitleStmt = tree.find(".//dhd:titleStmt", NAMESPACE_XML)
    return [_redirectWrongIds(person.get("ref")[1:]) for person in nodeTitleStmt.findall("./dhd:author", NAMESPACE_XML)]  # authors ids without hashtag


def _getKeywordIdByName(dictKeyword, keywordText):
    # search for existing keyword
    for keyword in dictKeyword.values():
        if keyword["text"] == keywordText:
            keyword["frequency"] += 1
            return keyword["id"]

    # create new keyword
    keywordID = str(uuid.uuid1())
    dictKeyword[keywordID] = {
        "id": keywordID,
        "text": keywordText,
        "frequency": 1
    }
    return keywordID


def _redirectWrongIds(personID):
    if personID in PERSON_ID_LOOKUP_DICT:
        return PERSON_ID_LOOKUP_DICT[personID]
    else:
        return personID
