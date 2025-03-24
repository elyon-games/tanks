from common.time import get_current_time_ms
import common.random
from server.services.network.packets import Packet

class Gateway:
    def __init__(self, userID):
        self.id = common.random.generate_random_code()
        self.SECRET_KEY = common.random.generate_random_string(48)
        self.userID: str = userID
        self.groups: list[str] = []
        self.status: str = "init"
        self.last_update = get_current_time_ms()
        self.packets: list[Packet] = []

    # fonction pour ajouter un groupe
    def add_group(self, group):
        self.groups.append(group)

    # fonction pour supprimer un groupe
    def remove_group(self, group):
        self.groups.remove(group)
    
    # fonction pour vérifier si le gateway a un groupe donné
    def has_group(self, group):
        return group in self.groups

    # fonction pour mettre à jour le gateway
    def update(self):
        if self.status == "close" or self.status == "expired" or self.status == "init":
            raise ConnectionError("GATWAY_NOT_CONNECTED")
        self.last_update = get_current_time_ms()

    # fonction pour vérifier la clé du gateway
    def verify_key(self, key):
        if key == self.SECRET_KEY:
            return True
        raise ConnectionError("GATEWAY_KEY_NOT_VALID")

    # fonction pour connecter le gateway
    def connect(self):
        if self.status == "connected":
            raise ConnectionError("GATEWAY_ALREADY_CONNECTED")
        if self.status == "close":
            raise ConnectionError("GATEWAY_CLOSED")
        self.status = "connected"
        self.update()

    # fonction pour vérifier si le gateway est expiré
    def is_expired(self):
        if self.status != "connected":
            return False
        if get_current_time_ms() - self.last_update > 10000:
            self.status = "expired"
            return True
        return False

    # fonction pour vérifier si le gateway est bon
    def is_good(self):
        return self.status == "connected"

    # fonction pour vérifier si le gateway est connecté
    def is_connected(self):
        return self.status == "connected"

    # fonction pour envoyer un message au client
    def send_message(self, datas):
        packet = Packet("server-to-client", datas)
        self.packets.append(packet)

    # fonction pour recevoir un message du client
    def receve_message(self, datas):
        packet = Packet("client-to-server", datas)
        self.packets.append(packet)

    # fonction pour obtenir un message par ID
    def get_message(self, id):
        for packet in self.packets:
            if packet.id == id:
                packet.status = "read"
                return {
                    "id": packet.id,
                    "time": packet.time,
                    "datas": packet.datas,
                    "type": packet.type
                }
        return None

    # fonction pour obtenir les messages
    def get_messages(self, type="all"):
        if type == "all":
            return self.packets
        return [self.get_message(packet.id) for packet in self.packets if packet.type == type and packet.status != "read"]

    # fonction pour fermer le gateway
    def close(self):
        if self.status == "close":
            return False
        self.status = "close"
                
gateways: list[Gateway] = []