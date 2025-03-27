import requests
from client.lib.utils import with_url_api, requestWithToken

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

def createParty() -> dict:
    data = None
    res = requestWithToken("GET", with_url_api(f"/parties/info/{id}"))
    if res.status_code == 200:
        data = res.json()["data"]

    