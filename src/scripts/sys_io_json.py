import json
import os

from constants import DATA_DIR

source = {
    "cache": {"dir": "./__cache__/", "path": "./__cache__/parser_{}.json"},
    "output": {"dir": DATA_DIR + "output/", "path": DATA_DIR + "output/output_{}.json"}
}


def write(source, data, title):
    if data is not None:
        _createDirectory(source["dir"])
        try:
            with open(source["path"].format(title), mode="w", encoding="utf-8") as file:
                file.write(json.dumps(data, ensure_ascii=False))
            return True
        except OSError as e:
            print(e)
            return False
    return False


def read(source, title):
    if hasFile(source, title):
        try:
            with open(source["path"].format(title), mode="r", encoding="utf-8") as file:
                data = json.load(file)
            return data
        except OSError as e:
            print(e)
            return None
    return None


def hasFile(source, title):
    return os.path.isfile(source["path"].format(title))


def hasFiles(source, titles):
    for title in titles:
        if not hasFile(source, title):
            return False
    return True


def _createDirectory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
