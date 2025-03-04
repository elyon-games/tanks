fonctions: list[dict] = []
class Fonction:
    def __init__(self, id: str, fnc):
        self.id: str = id
        self.fonction = fnc
    
    def run(self, userID: str, datas):
        self.fonction(userID, datas)