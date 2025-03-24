import requests
import common.random
from client.var import auth as authData
from client.lib.utils import with_url_api
from client.lib.utils import getHeadersWithToken

# Fonction pour créer une passerelle
def create_gateway() -> dict:
    try:
        response = requests.post(with_url_api("/client/gateway/create"), headers=getHeadersWithToken(token=authData.get("token", False)))
        response.raise_for_status()
        res: dict = response.json()["data"]
    except requests.exceptions.RequestException as e:
        return {"error": True, "message": str(e)}
    except ValueError:
        return {"error": True, "message": "Invalid JSON response"}

    return res