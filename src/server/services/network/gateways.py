import common.random

class Gateway:
    def __init__(self, userID):
        self.gateway_ID = common.random.generate_random_uuid()
        self.gateway_KEY = common.random.generate_random_string(32)
        self.userID = userID

    # server -> client

    def send_message(self, id, datas):
        pass

    # client -> server
    
    def appel_fonction(self, id, datas):
        for fonction in self.fonctions:
            if fonction["id"] == id:
                fonction["fonction"](self )
                
gateways: dict[str, Gateway] = {}
