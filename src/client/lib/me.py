import requests
from client.lib.utils import with_url_api
from client.var import auth as authData
from client.lib.utils import getHeadersWithToken

def getData():
    response: dict = requests.get(with_url_api("/users/me"), headers=getHeadersWithToken(token=authData.get("token", False)))
    res: dict = response.json()
    if response.status_code == 200 and not res.get("error", True):
        return {
            "error": True,
            "user": res.get("data", {})
        }
    return {"error": False}

def getUserData():
    pass