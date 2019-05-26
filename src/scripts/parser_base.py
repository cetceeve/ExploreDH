import os

dir = "../../data/TEI"

def readFiles():
    with os.scandir(dir) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.name.endswith('.xml') and entry.is_file():
                print(entry.name)
                # parse xml file here

if __name__ == "__main__":
    readFiles()