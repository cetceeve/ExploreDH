import json
import os

directory = "./__parsercache__/"
filename = directory + "cache_{}.json"

def write(data, title):
    if data is not None:
        createDirectory()
        try:
            with open(filename.format(title), mode="w", encoding="utf-8") as file:
                file.write(json.dumps(data, ensure_ascii=False))
            return True
        except OSError as e:
            print(e)
            return False
    return False


def read(title):
    if isFile(title):
        try:
            with open(filename.format(title), mode="r", encoding="utf-8") as file:
                data = json.load(file)
            return data
        except OSError as e:
            print(e)
            return None
    return None

def isFile(title):
    return os.path.isfile(filename.format(title))


def createDirectory():
    if not os.path.exists(directory):
       os.makedirs(directory, exist_ok=True)