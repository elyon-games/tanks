from urllib.parse import urljoin
from common.config import getConfig
from client.var import auth as authData
from client.lib.screen.controller import showScreen
from common.time import get_current_time
import requests

# Récupération de l'URL du serveur
host: str = getConfig("client")["server"]["host"]

# Fonction pour récupérer l'URL de l'API
def get_api_url() -> str:
    if not host:
        return None
    return f"http://{host}/api"

# Fonction pour joindre l'URL de l'API
def with_url_api(url: str) -> str:
    return f"{get_api_url()}{url}"

# Fonction pour ajouté le token dans les headers
def getHeadersWithToken(headers: dict = None, token: str = None) -> dict:
    if headers is None:
        headers = {}
    if not token:
        token = authData["token"]
    headers["Authorization"] = f"Bearer {authData['token'] if token is None else token}"
    return headers

# Fonction pour savoir si ont est sur le serveur officiel
def isOfficielServer():
    return host.split(":")[0].endswith("elyon.younity-mc.fr")

def requestWithToken(method: str, url: str, data: dict = None, headers: dict = None):
    headers = getHeadersWithToken(headers)
    if method == "GET":
        return requests.get(url, headers=headers, json=data)
    elif method == "POST":
        return requests.post(url, headers=headers, json=data)
    elif method == "PUT":
        return requests.put(url, headers=headers, json=data)
    elif method == "DELETE":
        return requests.delete(url, headers=headers, json=data)
    else:
        raise ValueError("Invalid HTTP method")

# Fonction pour récupérer l'ID d'un utilisateur avec son nom d'utilisateur
def getUserIDWithUsername(username: str) -> str:
    url = with_url_api(f"/users/id/{username}")
    res = requests.get(url)
    if res.status_code == 200:
        return res.json()["data"]
    return None

# Fonction pour récupérer les informations d'un utilisateur avec son ID
def getProfil(userID: int) -> dict:
    url = with_url_api(f"/users/{userID}")
    res = requests.get(url)
    if res.status_code == 200:
        return res.json()["data"]
    return None

def verifyStatusRes(res: dict):
    errorStatus = res.get("error", False)
    if errorStatus:
        showScreen("error", {
            "time": get_current_time(),
            "message": res.get("message", "Une erreur est survenue !"),
        })
    else:
        return res.get("data", {})

