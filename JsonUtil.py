import json
import pathlib

# https://docs.python.org/3/library/json.html


def loadJson(path: pathlib.PurePath) -> dict:
    with open(path) as json_file:
        json_data = json.load(json_file)
    return json_data


def saveJson(path: pathlib.PurePath, object: dict) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(object, f, ensure_ascii=False, indent=4)
