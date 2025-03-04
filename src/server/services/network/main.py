from server.services.network.packets import Packet, packets
from server.services.network.gateways import Gateway, gateways
from server.services.network.fonctions import Fonction, fonctions

def register_fonction(id, fonction) -> None:
    if id in fonctions:
        raise Exception("FONCTION_ALREADY_REGISTERED")
    fonctions.append({
        "id": id,
        "class": Fonction(id, fnc=fonction)
    })

def create_gateway(userID) -> Gateway:
    if userID in gateways :
        return {
            "error": True,
            "code": "ALREADY_CONNECTED"
        }
    gateways[userID] = Gateway(userID)
    return gateways[userID]
