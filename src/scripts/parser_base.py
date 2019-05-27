import os
import json
import parser_listperson as parserListPerson  
import parser_listorg as parserListOrga
import missing_entities_controller as MEC
import novatim_adapter as geocoder
import spacy_adapter as ner


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

    dictPerson = parserListPerson.parse(pathListPerson)
    dictOrga, dictLocation = parserListOrga.parse(pathListOrga)


    # ner.runNER("Language Technology Group, Universität Hamburg, Deutschland")
    # geocoder.getLocation("Universität Rostock")

    # print(json.dumps(dictPerson, indent=4, ensure_ascii=False))
    # MEC.writeMissingEntityInfoFile(dictPerson, dictOrga)
    # MEC.writeAdditionalEntityJSONFile(dictPerson, dictOrga)