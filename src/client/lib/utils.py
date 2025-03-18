from urllib.parse import urljoin
from common.config import getConfig
from client.var import auth as authData
import requests

host: str = getConfig("client")["server"]["host"]

def get_api_url() -> str:
    if not host:
        return None
    return f"http://{host}/api"

def with_url_api(url: str) -> str:
    return f"{get_api_url()}{url}"

def getHeadersWithToken(headers={}, token:str=""):
    headers["Authorization"] = f"Bearer {authData['token'] if not token else token}"
    return headers

def isOfficielServer():
    return host.split(":")[0].endswith("elyon.younity-mc.fr")

def getUserIDWithUsername(username: str) -> str:
    url = with_url_api(f"/users/id/{username}")
    res = requests.get(url)
    if res.status_code == 200:
        return res.json()["data"]
    return None

def getProfil(userID: int) -> dict:
    url = with_url_api(f"/users/{userID}")
    res = requests.get(url)
    if res.status_code == 200:
        return res.json()["data"]
    return None

def getMaps() -> list[dict]:
    url = with_url_api("/maps")
    res = requests.get(url)
    if res.status_code == 200:
        return res.json()["data"]
    return None
