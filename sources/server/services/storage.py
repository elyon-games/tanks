import json
from common.path import get_path
from common.utils import joinPath, create_file_if_not_exists

info_file_path = joinPath(get_path("server_data"), "info.json")

# Initialisation du stockage
def initStorage():
    create_file_if_not_exists(info_file_path, json.dumps({}))

# Fonctions de lecture de données
def readData():
    with open(info_file_path, "r") as file:
        return json.load(file)

# Fonctions d'écriture de données
def writeData(data):
    with open(info_file_path, "w") as file:
        json.dump(data, file)

# Fonctions pour savoir si une clé existe et pour obtenir sa valeur
def hasKey(key):
    data = readData()
    return key in data

# Fonctions pour obtenir et définir une valeur
def getValue(key):
    data = readData()
    return data.get(key)

# Fonctions pour définir une valeur
def setValue(key, value):
    data = readData()
    data[key] = value
    writeData(data)