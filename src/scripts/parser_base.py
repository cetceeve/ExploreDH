import os
import parser_listperson as parserListPerson

dirTEI = "../../data/TEI"
pathListPerson = "../../data/preprocessed/listperson.xml"

def readTEI():    
    with os.scandir(dirTEI) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.name.endswith('.xml') and entry.is_file():
                print(entry.name)
                # parse xml file here

def getDictPerson():
    return parserListPerson.parse(pathListPerson)

if __name__ == "__main__":
    # readTEI()

    getDictPerson()

    # get people with no associated organisation
    # testdict = getDictPerson()
    # for person in testdict.values():
    #     if "__temp__affil" in person:
    #         print(person)
