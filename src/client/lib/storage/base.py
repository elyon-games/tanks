import common.utils as utils
import common.path as path
import os
import json

class File:
    def __init__(self, id, path: str = None, default: dict = {}):
        self.id = id
        self.data = {}
        self.path = utils.joinPath(path, f"{self.id}.json")
        if self.existsData():
            self.loadData()
        else:
            self.data = default
            self.saveData()
    
    def setData(self, data: dict) -> None:
        self.data = data

    def addData(self, key: str, value) -> None:
        self.data[key] = value
    
    def updateData(self, key: str, value) -> None:
        self.data[key] = value

    def getKey(self, key: str):
        return self.data.get(key, None)

    def getData(self) -> dict:
        return self.data.copy()

    def existsData(self) -> bool:
        return os.path.exists(self.path)

    def saveData(self) -> None:
        utils.create_file_if_not_exists(self.path)
        with open(self.path, "w") as file:
            json.dump(self.data, file)

    def loadData(self) -> None:
        if not self.existsData():
            return
        with open(self.path, "r") as file:
            self.data = json.load(file)
    
    def removeData(self) -> None:
        os.remove(self.path)