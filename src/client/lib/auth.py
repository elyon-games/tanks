import requests
from client.lib.utils import with_url_api
from client.var import auth as authData
from client.lib.utils import getHeadersWithToken

def login(email, password):
    global authData
    response: dict = requests.post(with_url_api("/auth/login"), json={
        'email': email,
        'password': password
    }).json()
    if not response.get("token", None) or not response.get("message", None) == "CONNEXION_VALID":
        return False
    authData["token"] = response["token"]
    verifyData = verify(authData["token"])
    if verifyData["status"] == True:
        return True
    else: 
        return False
    
def register(para):
    pass

def verify(token):
    response: dict = requests.get(with_url_api("/auth/verify"), headers=getHeadersWithToken(token=token)).json()
    if response.get("message", None):
        if response.get("message") == "TOKEN_VALID":
            return {
                "status": True,
                "user_id": response.get("user_id", None)
            }
    return {"status": False}