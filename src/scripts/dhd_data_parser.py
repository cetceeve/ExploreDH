import os
import json
import parser_listperson as parserListPerson  
import parser_listorg as parserListOrga
import dhd2019_missing_entities_controller as MEC
import novatim_adapter as geocoder
import spacy_adapter as ner
import parser_cache as cache

import parser_peopleAtLocation as p_pal

dirTEI = "../../data/TEI"
pathListPerson = "../../data/preprocessed/listperson.xml"
pathListOrga = "../../data/preprocessed/listorg.xml"

def readTEI():
    with os.scandir(dirTEI) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.name.endswith('.xml') and entry.is_file():
                print(entry.name)
                # parse xml file here


if __name__ == "__main__":
    if cache.hasFile("dictPerson") and cache.hasFile("dictOrga") and cache.hasFile("dictLocation"):
        print("reading from cache")
        dictPerson = cache.read("dictPerson")
        dictOrga = cache.read("dictOrga")
        dictLocation = cache.read("dictLocation")
    else:
        print("parsing xml")
        dictPerson = parserListPerson.parse(pathListPerson)
        dictOrga, dictLocation = parserListOrga.parse(pathListOrga)
        print("fixing entities")
        MEC.getAdditionalEntities(dictPerson, dictOrga, dictLocation)
        MEC.fixTimGeelhaar(dictPerson)

        print("writing to cache")
        cache.write(dictPerson, "dictPerson")
        cache.write(dictOrga, "dictOrga")
        cache.write(dictLocation, "dictLocation")


    # p_pal.printPeopleAtLocation(dictPerson, dictOrga, dictLocation)
    # readTEI()

    # ner.runNER("Language Technology Group, Universität Hamburg, Deutschland")
    # geocoder.getLocation("Nürnberg, Deutschland")

    # print(json.dumps(dictPerson, indent=4, ensure_ascii=False))
    # print(json.dumps(dictOrga, indent=4, ensure_ascii=False))
    # print(json.dumps(dictLocation, indent=4, ensure_ascii=False))
