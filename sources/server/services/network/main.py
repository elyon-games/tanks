from server.services.network.gateways import Gateway, gateways

# fonction pour créer un gateway s'il n'existe pas déjà
def create_gateway(userID) -> Gateway:
    test = get_gateway_by_user(userID)
    if test and test.status not in ["close", "expired"]:
        raise Exception("GATEWAY_ALREADY_EXISTS")
    gateway = Gateway(userID)
    gateways.append(gateway)
    return gateway

# fonction pour obtenir un gateway par ID
def get_gateway(gatewayID: str) -> Gateway:
    for gateway in gateways:
        if gateway.id == gatewayID:
            return gateway
    return None

# fonction pour obtenir un gateway par utilisateur
def get_gateway_by_user(userID: str) -> Gateway:
    for gateway in gateways:
        if gateway.userID == userID:
            return gateway
    return None

def send_message_to_gateway(gatewayID: str, datas: dict):
    gateway = get_gateway(gatewayID)
    if gateway:
        gateway.send_message(datas)
        return True
    return False

def send_message_to_user(userID: str, datas: dict):
    gateway = get_gateway_by_user(userID)
    if gateway:
        gateway.send_message(datas)
        return True
    return False

def send_message_to_all(datas: dict):
    for gateway in gateways:
        gateway.send_message(datas)
    return True

def send_message_to_group(groupID: str, datas: dict):
    for gateway in gateways:
        if groupID in gateway.groups:
            gateway.send_message(datas)
    return True