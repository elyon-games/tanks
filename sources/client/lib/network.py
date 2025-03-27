from client.var import auth as authData
from client.var import gateway as gatewayData
from client.lib.utils import requestWithToken, with_url_api

lastMessage = None

def connect_gateway(gateway_id: int, gateway_key: str) -> dict:
    res = requestWithToken("POST", with_url_api("/client/gateway/connect"), {
        "gateway_id": gateway_id,
        "gateway_key": gateway_key,
    })
    if res.status_code == 200:
        data = res.json()["data"]
        gatewayData["id"] = gateway_id
        gatewayData["key"] = gateway_key
        gatewayData["status"] = True
        return data
    return None

def close_gateway():
    pass

def getStatus_gateway():
    return gatewayData["status"]

def receive_messages():
    res = requestWithToken("POST", with_url_api("/client/gateway/update"), {
        "gateway_id": gatewayData["id"],
        "gateway_key": gatewayData["key"],
    })
    if res.status_code == 200:
        data = res.json()["data"]
        
        return packets

def send_message(datas):
    