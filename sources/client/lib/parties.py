from client.lib.utils import with_url_api, requestWithToken
from client.lib.gateway import connect_gateway

def getPartyInfo(id: int) -> dict:
    res = requestWithToken("GET", with_url_api(f"/parties/info/{id}"))
    if res.status_code == 200:
        return res.json()["data"]
    return None

def getPartysPublicShow() -> list:
    res = requestWithToken("GET", with_url_api("/parties/public"))
    if res.status_code == 200:
        return res.json()["data"]
    return []

def joinParty(private: bool = False, id: int = None) -> dict:
    if private and id is None:
        raise ValueError("ID is required for private party")

    payload = {"private": private}
    if private:
        payload["party_id"] = id

    res = requestWithToken("POST", with_url_api("/parties/join"), payload)
    if res.status_code == 200:
        data = res.json()["data"]
        connect_gateway(data["gateway_id"], data["gateway_key"])
        return data
    return None


def createPrivateParty(map: int = 1) -> dict:
    res = requestWithToken("GET", with_url_api("/parties/create"), {
        "map": map,
    })
    if res.status_code == 200:
        data = res.json()["data"]

    