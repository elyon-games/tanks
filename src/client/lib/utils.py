from urllib.parse import urljoin
from common.config import getConfig
from client.var import auth as authData
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
def getHeadersWithToken(headers={}, token:str=""):
    headers["Authorization"] = f"Bearer {authData['token'] if not token else token}"
    return headers

# Fonction pour savoir si ont est sur le serveur officiel
def isOfficielServer():
    return host.split(":")[0].endswith("elyon.younity-mc.fr")

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

# Fonction pour récupérer les maps
def getMaps() -> list[dict]:
    url = with_url_api("/maps")
    res = requests.get(url)
    if res.status_code == 200:
        return res.json()["data"]
    return None
