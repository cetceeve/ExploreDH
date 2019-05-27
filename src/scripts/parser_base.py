import os
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
    # readTEI()#

    dictPerson = parserListPerson.parse(pathListPerson)
    dictOrga, dictLocation = parserListOrga.parse(pathListOrga)

    # ner.runNER("Language Technology Group, Universität Hamburg, Deutschland")
    # geocoder.getLocation("Universität Rostock")

    # get people with no associated organisation
    # for person in dictPerson.values():
    #     if "__temp__affil" in person:
    #         print(person)

    # get orgas with no location
    # for orga in dictOrga.values():
    #     if "location" not in orga:
    #         print(orga)
