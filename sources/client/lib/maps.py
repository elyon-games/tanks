import requests
from client.lib.utils import with_url_api

maps: list[dict] = []

# Fonction pour récupérer les maps
def getMaps() -> list[dict]:
    global maps
    url = with_url_api("/maps")
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()["data"]
        maps = data
        return data
    return None

# Fonction pour récupérer une map avec son ID
def getMap(id: int) -> dict:
    global maps
    if not maps:
        getMaps()
    for map in maps:
        if map["id"] == id:
            return map
    return None

