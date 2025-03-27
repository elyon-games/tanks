from client.var import auth as authData
from client.var import gateway as gatewayData
from client.lib.utils import requestWithToken, with_url_api

def connect_gateway(gateway_id: int, gateway_key: str) -> dict:
    res = requestWithToken("POST", with_url_api("/client/gateway/connect"), {
        "gateway_id": gateway_id,
        "gateway_key": gateway_key,
    })
    if res.status_code == 200:
        data = res.json()["data"]
        gatewayData["id"] = gateway_id
        gatewayData["key"] = gateway_key
        print(data)
        return data
    return None

def update_gateway(data: dict):
    res = requestWithToken("PUT", with_url_api("/client/gateway/update"), {
        "gateway_id": gatewayData["id"],
        "gateway_key": gatewayData["key"],
    })
    if res.status_code == 200:
        data = res.json()["data"]
        gatewayData["id"] = data["gateway_id"]
        gatewayData["key"] = data["gateway_key"]
        return data

