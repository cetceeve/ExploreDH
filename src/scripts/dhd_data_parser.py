import os
import json

import parser_tei as parserTei
import parser_listperson as parserListPerson  
import parser_listorg as parserListOrga
import dhd2019_missing_entities_controller as MEC
import novatim_adapter as geocoder
import spacy_adapter as ner
import parser_io as io
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
    if io.hasFile(io.source["cache"], "dictPerson") and io.hasFile(io.source["cache"], "dictOrga") and io.hasFile(io.source["cache"], "dictLocation"):
        print("reading from cache")
        dictPerson = io.read(io.source["cache"], "dictPerson")
        dictOrga = io.read(io.source["cache"], "dictOrga")
        dictLocation = io.read(io.source["cache"], "dictLocation")
    else:
        print("parsing xml")
        parserListPerson.parse(DATA_DIR + "preprocessed/listperson.xml", dictPerson)
        parserListOrga.parse(DATA_DIR + "preprocessed/listorg.xml", dictOrga, dictLocation)
        print("fixing entities")
        MEC.getAdditionalEntities(dictPerson, dictOrga, dictLocation)
        MEC.fixTimGeelhaar(dictPerson)
        MEC.addWalterScholger(dictPerson)

        print("writing to cache")
        io.write(io.source["cache"], dictPerson, "dictPerson")
        io.write(io.source["cache"], dictOrga, "dictOrga")
        io.write(io.source["cache"], dictLocation, "dictLocation")


    readTEI()
    # p_pal.printPeopleAtLocation(dictPerson, dictOrga, dictLocation)

    # ner.runNER("Language Technology Group, Universität Hamburg, Deutschland")
    # geocoder.getLocation("Nürnberg, Deutschland")

    # print(json.dumps(dictKeyword, indent=4, ensure_ascii=False))