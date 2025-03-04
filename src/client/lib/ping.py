import requests
from client.lib.utils import with_url_api

def ping() -> dict:
    try:
        response = requests.get(with_url_api("/client/info"))
        response.raise_for_status()
        res: dict = response.json()
    except requests.exceptions.RequestException as e:
        return {"error": True, "message": str(e)}
    except ValueError:
        return {"error": True, "message": "Invalid JSON response"}

    if res.get("error"):
        if res["error"] == True:
            return {"error": True}
    return res