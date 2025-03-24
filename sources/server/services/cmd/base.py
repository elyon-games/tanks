from typing import TypedDict, List

class ArgDict(TypedDict):
    require: bool
    id: str
    description: str
    type: str

class classCMD:
    def __init__(self, description: str = "", args: List[ArgDict] = []):
        self.args = args
        self.description = description

    def run(self):
        pass

    def getDescription(self):
        return self.description
    
    def getParameters(self):
        return [f"{arg['id']} ({arg['type']}): {arg['description']} - {'Required' if arg['require'] else 'Optional'}" for arg in self.args]

    def getMissingArgs(self, argsToTest):
        missingArgs = []
        for required_arg in self.getRequireArgs():
            found = False
            for arg in argsToTest:
                if arg["id"] == required_arg["id"]:
                    found = True
                    break
            if not found:
                missingArgs.append(required_arg["id"])
        return missingArgs

    def getUnknownArgs(self, argsToTest):
        unknownArgs = []
        for arg in argsToTest:
            known = False
            for known_arg in self.args:
                if arg["id"] == known_arg["id"]:
                    known = True
                    break
            if not known:
                unknownArgs.append(arg["id"])
        return unknownArgs

    def getRequireArgs(self):
        return [arg for arg in self.args if arg["require"] == True]
    
    def getOptionalArgs(self):
        return [arg for arg in self.args if arg["require"] == False]