import sys
import os
import json

import parser_tei as parserTei
import parser_listperson as parserListPerson 
import parser_listorg as parserListOrga
import dhd2019_missing_entities_controller as MEC
import novatim_adapter as geocoder
import spacy_adapter as ner
import sys_io_json as io
import parser_peopleAtLocation as p_pal

from constants import DATA_DIR

dictPerson = {}
dictOrga = {}
dictLocation = {}
dictArticle = {}
dictKeyword = {}


def readTEI():
    with os.scandir(DATA_DIR + "TEI/") as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.name.endswith('.xml') and entry.is_file():
                parserTei.parse(entry.path, dictPerson, dictArticle, dictKeyword)


if __name__ == "__main__":
    reload_cache = False
    if len(sys.argv) > 1:
        if sys.argv[1] == "-r" or sys.argv[1] == "-reload-cache":
            reload_cache = True

    if io.hasFiles(io.source["cache"], ["dictPerson", "dictOrga", "dictLocation", "dictArticle", "dictKeyword"]) and not reload_cache:
        print("reading from cache")
        dictPerson = io.read(io.source["cache"], "dictPerson")
        dictOrga = io.read(io.source["cache"], "dictOrga")
        dictLocation = io.read(io.source["cache"], "dictLocation")
        dictArticle = io.read(io.source["cache"], "dictArticle")
        dictKeyword = io.read(io.source["cache"], "dictKeyword")
    else:
        print("parsing xml")
        parserListPerson.parse(os.path.abspath(DATA_DIR + "preprocessed/listperson.xml"), dictPerson)
        parserListOrga.parse(os.path.abspath(DATA_DIR + "preprocessed/listorg.xml"), dictOrga, dictLocation)
        print("fixing entities")
        MEC.getAdditionalEntities(dictPerson, dictOrga, dictLocation)
        MEC.fixTimGeelhaar(dictPerson)
        MEC.addWalterScholger(dictPerson)
        print("parsing TEI")
        readTEI()

        print("writing to cache")
        io.write(io.source["cache"], dictPerson, "dictPerson")
        io.write(io.source["cache"], dictOrga, "dictOrga")
        io.write(io.source["cache"], dictLocation, "dictLocation")
        io.write(io.source["cache"], dictArticle, "dictArticle")
        io.write(io.source["cache"], dictKeyword, "dictKeyword")


    # p_pal.printPeopleAtLocation(dictPerson, dictOrga, dictLocation)

    # ner.runNER("Language Technology Group, Universität Hamburg, Deutschland")
    # geocoder.getLocation("Nürnberg, Deutschland")

    # print(json.dumps(dictLocation, indent=4, ensure_ascii=False))