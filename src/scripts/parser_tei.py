import xml.etree.ElementTree as ET
import uuid

from constants import NAMESPACE
_abstract = "Butterfly seems like it is in line with the aesthetics we got in their pre-debut works. It also features a mature sound and stands out for a variety of reasons. The first is the song’s instrumental. The song takes on EDM in a very unique manner. It combines different sounds together to create a very dynamically powerful instrumentation that really allows for the chorus to stand out. I also like how they used a very high pitched ‘Fly Like A Butterfly’ as part of the chorus. It does sound like screeching but you can make out the words and it really adds a depth of colour to the song. The second reason would have to be the vocals. It is that one line again that I think really makes the song stand out, this time slightly lower pitch for the members to be able to sing. The rapping also has to be commended as it isn’t a powerful approach but rather more delicate. But it works well with the rest of the song. I also found it rather interesting that the vocals/raps were minimalistic, as it is usually the instrumental. The third and final reason why the song stands out is the lyrics. They are all about finding oneself and usually, songs of this nature earn applause from me. Overall, Butterfly is uniquely different but so amazing."

def parse(path, dictPerson, dictArticle, dictKeyword):
    tree = ET.parse(path)

    # Panels cannot be taken into account
    if tree.find(".//dhd:profileDesc/dhd:textClass/dhd:keywords[@n='subcategory']/dhd:term", NAMESPACE).text == "Panel":
        return None

    _getEmails(tree, dictPerson)
    _getArticle(tree, dictArticle, dictKeyword)


def _getEmails(tree, dictPerson):
    nodeTitleStmt = tree.find(".//dhd:titleStmt", NAMESPACE)

    for person in nodeTitleStmt.findall("./dhd:author", NAMESPACE):
        personId = _redirectWrongIds(person.get("ref")[1:]) # remove hashtag from ref
        
        if "email" not in dictPerson[personId]:
            dictPerson[personId]["email"] = [person.find("./dhd:email", NAMESPACE).text]
        elif person.find("./dhd:email", NAMESPACE).text not in dictPerson[personId]["email"]:
            dictPerson[personId]["email"].append(person.find("./dhd:email", NAMESPACE).text)


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
    nodeTitle = tree.find(".//dhd:titleStmt/dhd:title[@type='full']", NAMESPACE)

    if nodeTitle is not None:
        fullTitle = nodeTitle.find("./dhd:title[@type='main']", NAMESPACE).text
        subTitle = nodeTitle.find("./dhd:title[@type='sub']", NAMESPACE).text
        if subTitle is not None:
            fullTitle += ": " + subTitle
        return fullTitle
    else:
        return tree.find(".//dhd:titleStmt/dhd:title", NAMESPACE).text


def _getKeywords(tree, dictKeyword):
    keywords = []
    #find keywords/topics
    nodeProfileDesc = tree.find(".//dhd:profileDesc", NAMESPACE)
    for element in nodeProfileDesc.findall(".//dhd:textClass/dhd:keywords", NAMESPACE):
        if element.attrib["n"] == "keywords" or element.attrib["n"] == "topics":
            for term in element.findall("./dhd:term", NAMESPACE):
                keywords.append(_getKeywordIdByName(dictKeyword, term.text))
    return keywords


def _getAuthors(tree):
    authors = []
    nodeTitleStmt = tree.find(".//dhd:titleStmt", NAMESPACE)

    for person in nodeTitleStmt.findall("./dhd:author", NAMESPACE):
        authors.append(_redirectWrongIds(person.get("ref")[1:])) # remove hashtag from ref
    return authors


def _getKeywordIdByName(dictKeyword, keywordText):
    # search for existing keyword
    for element in dictKeyword.values():
        if element["text"] == keywordText:
            element["frequency"] += 1
            return element["id"]

    # create new keyword
    keywordID = str(uuid.uuid1())
    dictKeyword[keywordID] = {
        "id": keywordID,
        "text": keywordText,
        "frequency": 1
    }
    return keywordID
    


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