import json
from common.config import getConfig
from common.path import get_path
from common.utils import joinPath, create_file_if_not_exists

info_file_path = joinPath(get_path("server_data"), "info.json")

def initStorage():
    create_file_if_not_exists(info_file_path, json.dumps({}))

def readData():
    with open(info_file_path, "r") as file:
        return json.load(file)

def writeData(data):
    with open(info_file_path, "w") as file:
        json.dump(data, file)

def hasKey(key):
    data = readData()
    return key in data

def getValue(key):
    data = readData()
    return data.get(key)

def setValue(key, value):
    data = readData()
    data[key] = value
    writeData(data)