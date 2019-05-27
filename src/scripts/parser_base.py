import os
import json
import parser_listperson as parserListPerson  
import parser_listorg as parserListOrga

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

    # writeMissingEntityInfoFile(dictPerson, dictOrga)
    

def writeMissingEntityInfoFile(dictPerson, dictOrga):
    file = open("dhd2019_missing_info.txt", mode="w", encoding="utf-8")

    file.write("Personen ohne Organisation:")
    # get people with no associated organisation
    for person in dictPerson.values():
        if "__temp__affil" in person:
            file.write("\n" + json.dumps(person, indent=4, ensure_ascii=False))
    
    file.write("\n\nLocations ohne Koordinaten:")
    # get orgas with no location
    for orga in dictOrga.values():
        if "location" not in orga:
            file.write("\n" + json.dumps(orga, indent=4, ensure_ascii=False))

    file.close()