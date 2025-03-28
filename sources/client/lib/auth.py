import requests
import common.config as config
from client.lib.utils import with_url_api
from client.var import auth as authData
from client.lib.utils import getHeadersWithToken
from client.lib.screen.controller import showScreen
from client.lib.storage.controller import getStorage

# Fonction pour se connecter
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

# Fonction pour s'inscrire
def register(para):
    pass

# Fonction pour vérifier le token
def verify(token):
    response: dict = requests.get(with_url_api("/auth/verify"), headers=getHeadersWithToken(token=token)).json()
    if response.get("message", None):
        if response.get("message") == "TOKEN_VALID":
            return {
                "status": True,
                "user_id": response.get("user_id", None)
            }
    return {"status": False}

# Fonction pour se déconnecter
def logout():
    global authData
    getStorage(config.getConfig("server").get("server", {}).get("id", None)).removeData()
    authData["token"] = None
    showScreen("auth-login")
    return True