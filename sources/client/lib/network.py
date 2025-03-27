from client.var import auth as authData
from client.lib.utils import requestWithToken, with_url_api

def connect_gateway(gateway_id: int, gateway_key: str) -> dict:
    res = requestWithToken("POST", with_url_api("/gateway/connect"), {
        "gateway_id": gateway_id,
        "gateway_key": gateway_key,
    })
