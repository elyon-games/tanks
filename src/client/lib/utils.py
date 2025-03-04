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
