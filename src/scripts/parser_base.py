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


def writeAdditionalEntityJSONFile(dictPerson, dictOrga):
    with open("dhd2019_additional_entities.json", mode="w", encoding="utf-8") as file:
        peopleMissingOrgas = []
        additionalOrgas = []
        orgasMissingLocations = []
        res = {
            "peopleMissingOrgas": peopleMissingOrgas,
            "additionalOrgas": additionalOrgas,
            "orgasMissingLocations": orgasMissingLocations
        }

        # get people with no associated organisation
        counter = 148
        for person in dictPerson.values():
            if "__temp__affil" in person:
                person["organisation"] = "org__" + str(counter)
                counter += 1

                peopleMissingOrgas.append(person)

        # create new organisations
        for i in range(4):
            additionalOrgas.append({
                "id": "org__" + str(148 + i),
                "name": "{{enter useful organisation name e.g. Germanisches Nationalmuseum, Nürnberg }}",
                "locationame": "{{enter city name here (will be processed by novatim) z.B. Nürnberg}}"
            })

        # get orgas with no location
        for orga in dictOrga.values():
            if "location" not in orga:
                orgasMissingLocations.append({
                    "id": orga["id"],
                    "name": orga["name"],
                    "city": "{{enter city name here (will be processed by novatim)  z.B. Würzburg}}"
                })
        
        file.write(json.dumps(res, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    # readTEI()

    dictPerson = parserListPerson.parse(pathListPerson)
    dictOrga, dictLocation = parserListOrga.parse(pathListOrga)


    # ner.runNER("Language Technology Group, Universität Hamburg, Deutschland")
    # geocoder.getLocation("Universität Rostock")

    # print(json.dumps(dictPerson, indent=4, ensure_ascii=False))
    # writeMissingEntityInfoFile(dictPerson, dictOrga)
    writeAdditionalEntityJSONFile(dictPerson, dictOrga)