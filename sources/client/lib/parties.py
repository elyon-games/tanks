import requests
from client.lib.utils import with_url_api

def getPartyInfo(id: int):
    url = with_url_api(f"/parties/info/{id}")
    res = requests.get(url)
    if res.status_code == 200:
        return res.json()["data"]
    return None