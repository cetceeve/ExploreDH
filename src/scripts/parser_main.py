import sys
import os
import json
import re

import parser_tei as parserTei
import parser_listperson as parserListPerson
import parser_listorg as parserListOrga
import dhd2019_missing_entities_controller as MEC
import novatim_adapter as geocoder
import sys_io_json as io
import parser_sql_db_creator as sql_creator
from spacy_adapter import SpacyNER
from parser_keyword_similarity import KeywordSimilarity
from processing_organetwork import OrgaNetwork

from constants import DATA_DIR

dictPerson = {}
dictOrga = {}
dictLocation = {}
dictArticle = {}
dictKeyword = {}


def _fixErrorsInPreprocessedXML():
    MEC.getAdditionalEntities(dictPerson, dictOrga, dictLocation)
    MEC.fixTimGeelhaar(dictPerson)
    MEC.addWalterScholger(dictPerson)


def _parseTEI():
    with os.scandir(DATA_DIR + "TEI/") as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.name.endswith('.xml') and entry.is_file():
                parserTei.parse(entry.path, dictPerson, dictArticle, dictKeyword)


def _mergeSimilarKeywords():
    similarKeywords = KeywordSimilarity(dictKeyword).getSimilarKeywords()
    for keywordTuple in similarKeywords:
        _mergeKeywordTuple(keywordTuple)

    # cleanup leftover property from processing
    for keyword in dictKeyword.values():
        del keyword["_stem"]


def _mergeKeywordTuple(keywordTuple):
    newKeywordID = keywordTuple[-1]
    oldKeywordIDs = keywordTuple[:-1]
    # replace old ids in articles
    for article in dictArticle.values():
        for kID in article["keywords"]:
            if kID in oldKeywordIDs:
                kID = newKeywordID

    # merge keyword frequency
    oldKeywords = [dictKeyword[kID] for kID in oldKeywordIDs]
    dictKeyword[newKeywordID]["frequency"] += sum([keyword["frequency"] for keyword in oldKeywords])

    # clean keyword dictionary
    for oldId in oldKeywordIDs:
        del dictKeyword[oldId]


def _addPreciseCoordinatesToOrgas():
    print("loading spacy...")
    ner = SpacyNER()
    for orga in dictOrga.values():
        # attempt geocoding directly on orga name
        res = geocoder.getLocation(orga["name"])
        if res is not None:
            orga["lat"] = res["lat"]
            orga["lon"] = res["lon"]
        else:
            # NER preprocessing step before geocoding
            data = _getLocationWithPreprocessedName(ner, orga["name"])
            if data is not None:
                orga["lat"] = data["lat"]
                orga["lon"] = data["lon"]
            else:
                # all attempts failed, just copy coords from location
                orga["lat"] = dictLocation[orga["location"]]["lat"]
                orga["lon"] = dictLocation[orga["location"]]["lon"]


def _getLocationWithPreprocessedName(ner, query):
    for entity in ner.runNER(query):
        # token should be of type ORG, to avoid using falls classifications a simple regex check is used
        if entity[0] == "ORG" and re.search(r"\w*(universit|hochschule)\w*", entity[1], flags=re.IGNORECASE):
            res = geocoder.getLocation(entity[1])
            if res is not None:
                return res
    return None


if __name__ == "__main__":
    # read from cache if files are present and no reparse was forced by user
    if io.hasFiles(io.source["cache"], ["dictPerson", "dictOrga", "dictLocation", "dictArticle", "dictKeyword"]) and not "-r" in sys.argv:
        print("reading from cache")
        dictPerson = io.read(io.source["cache"], "dictPerson")
        dictOrga = io.read(io.source["cache"], "dictOrga")
        dictLocation = io.read(io.source["cache"], "dictLocation")
        dictArticle = io.read(io.source["cache"], "dictArticle")
        dictKeyword = io.read(io.source["cache"], "dictKeyword")
    else:
        print("parsing preprocessed xml")
        parserListPerson.parse(os.path.abspath(DATA_DIR + "preprocessed/listperson.xml"), dictPerson)
        parserListOrga.parse(os.path.abspath(DATA_DIR + "preprocessed/listorg.xml"), dictOrga, dictLocation)
        print("fixing errors in preprocessed xml")
        _fixErrorsInPreprocessedXML()
        print("parsing TEI")
        _parseTEI()
        print("merging similar keywords")
        _mergeSimilarKeywords()
        print("adding coordinates to orgas")
        _addPreciseCoordinatesToOrgas()
        print("writing to cache")
        io.write(io.source["cache"], dictPerson, "dictPerson")
        io.write(io.source["cache"], dictOrga, "dictOrga")
        io.write(io.source["cache"], dictLocation, "dictLocation")
        io.write(io.source["cache"], dictArticle, "dictArticle")
        io.write(io.source["cache"], dictKeyword, "dictKeyword")

    # sql database
    if "-d" in sys.argv:
        # check for folder
        if not os.path.exists(DATA_DIR + "db"):
            os.mkdir(DATA_DIR + "db")
        # check for already existing db
        if os.path.exists(DATA_DIR + "db/dhd_data.db"):
            os.remove(DATA_DIR + "db/dhd_data.db")
        # create new database
        sql_creator.create_db(os.path.abspath(DATA_DIR + "db/dhd_data.db"), dictPerson, dictOrga, dictLocation, dictArticle, dictKeyword)
