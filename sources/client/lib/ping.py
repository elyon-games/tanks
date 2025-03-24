import requests
from client.lib.utils import with_url_api

# Fonction pour vérifier la connexion avec le serveur
def ping() -> dict:
    try:
        response = requests.get(with_url_api("/client/info"))
        response.raise_for_status()
        res: dict = response.json()
    # Gestion des erreurs
    except requests.exceptions.RequestException as e:
        return {"error": True, "message": str(e)}
    except ValueError:
        return {"error": True, "message": "Invalid JSON response"}

    # Vérification de la réponse
    if res.get("error"):
        if res["error"] == True:
            return {"error": True}
    return res