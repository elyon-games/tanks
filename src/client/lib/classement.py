import requests
from client.lib.utils import with_url_api
from client.var import auth as authData
from client.lib.utils import getHeadersWithToken

def getClassement(type: str, page: int = 1, per_page: int = 10) -> dict:
    response: dict = requests.get(with_url_api(f"/classement/{type}?page={page}&per_page={per_page}"), headers=getHeadersWithToken(token=authData.get("token", False)))
    res: dict = response.json()
    if response.status_code == 200 and not res.get("error", True):
        return res.get("data", {}).get("users", [])
    else:
        return {"error": True, "message": res.get("message", "Une erreur est survenue.")}

def getClassementKills(page: int = 1, per_page: int = 10) -> dict:
    return getClassement("kills", page, per_page).get("data", {})

def getClassementDeaths(page: int = 1, per_page: int = 10) -> dict:
    return getClassement("deaths", page, per_page)

def getClassementKD(page: int = 1, per_page: int = 10) -> dict:
    return getClassement("kd", page, per_page).get("data", {})

def getClassementWins(page: int = 1, per_page: int = 10) -> dict:
    return getClassement("wins", page, per_page).get("data", {})

def getClassementLoses(page: int = 1, per_page: int = 10) -> dict:
    return getClassement("loses", page, per_page).get("data", {})

def getClassementWL(page: int = 1, per_page: int = 10) -> dict:
    return getClassement("wl", page, per_page).get("data", {})

def getClassementPoints(page: int = 1, per_page: int = 10) -> dict:
    return getClassement("points", page, per_page).get("data", {})