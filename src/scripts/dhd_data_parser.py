import os
import json
import parser_listperson as parserListPerson  
import parser_listorg as parserListOrga
import dhd2019_missing_entities_controller as MEC
import novatim_adapter as geocoder
import spacy_adapter as ner
import parsercache as cache

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
    # readTEI()

    if cache.isFile("dictPerson") and cache.isFile("dictOrga") and cache.isFile("dictLocation"):
        dictPerson = cache.read("dictPerson")
        dictOrga = cache.read("dictOrga")
        dictLocation = cache.read("dictLocation")
    else:
        dictPerson = parserListPerson.parse(pathListPerson)
        dictOrga, dictLocation = parserListOrga.parse(pathListOrga)
        MEC.getAdditionalEntities(dictPerson, dictOrga, dictLocation)

        cache.write(dictPerson, "dictPerson")
        cache.write(dictOrga, "dictOrga")
        cache.write(dictLocation, "dictLocation")

    # ner.runNER("Language Technology Group, Universität Hamburg, Deutschland")
    # geocoder.getLocation("Nürnberg, Deutschland")

    # print(json.dumps(dictPerson, indent=4, ensure_ascii=False))
    # print(json.dumps(dictOrga, indent=4, ensure_ascii=False))
    # print(json.dumps(dictLocation, indent=4, ensure_ascii=False))
