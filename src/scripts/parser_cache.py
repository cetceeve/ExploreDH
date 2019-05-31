import json
import os

_directory = "./__parsercache__/"
_filename = _directory + "cache_{}.json"

def write(data, title):
    if data is not None:
        _createDirectory()
        try:
            with open(_filename.format(title), mode="w", encoding="utf-8") as file:
                file.write(json.dumps(data, ensure_ascii=False))
            return True
        except OSError as e:
            print(e)
            return False
    return False


def read(title):
    if hasFile(title):
        try:
            with open(_filename.format(title), mode="r", encoding="utf-8") as file:
                data = json.load(file)
            return data
        except OSError as e:
            print(e)
            return None
    return None


def hasFile(title):
    return os.path.isfile(_filename.format(title))


def _createDirectory():
    if not os.path.exists(_directory):
       os.makedirs(_directory, exist_ok=True)