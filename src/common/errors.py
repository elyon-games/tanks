errors_list = [
    {"code": "INVALID_REQUEST", "message": "Mauvaise Requête"},
    {"code": "UNAUTHORIZED", "message": "Non Autorisé"},
    {"code": "FORBIDDEN", "message": "Interdit"},
    {"code": "NOT_FOUND", "message": "Non Trouvé"},
    {"code": "METHOD_NOT_ALLOWED", "message": "Méthode Non Autorisée"},
    {"code": "REQUEST_TIMEOUT", "message": "Temps d'Attente Écoulé"},
    {"code": "TOO_MANY_REQUESTS", "message": "Trop de Requêtes"},
    {"code": "INTERNAL_SERVER_ERROR", "message": "Erreur Interne du Serveur"},
    {"code": "BAD_GATEWAY", "message": "Mauvaise Passerelle"},
    {"code": "SERVICE_UNAVAILABLE", "message": "Service Indisponible"},
    {"code": "GATEWAY_TIMEOUT", "message": "Temps d'Attente de la Passerelle Écoulé"},
    {"code": "CLIENT_VERSION_MISMATCH", "message": "La version du serveur ne correspond pas à celle du client."},
    {"code": "SERVER_MISSING_KEY", "message": "Le serveur n'a pas renvoyé de clé."},
    {"code": "ALREADY_CONNECTED", "message": "Vous êtes déjà connecté depuis une autre connexion."}
]

def generateError(code, message: str):
    for error in errors_list:
        if error["code"] == code:
            return {
                "status": False,
                "error": True,
                "code": code,
                "message": message
            }
    return {
        "status": False,
        "error": True,
        "code": "UNKNOWN_ERROR",
        "message": "Erreur Inconnue"
    }

def getError(code):
    for error in errors_list:
        if error["code"] == code:
            return error
    return {
        "code": "UNKNOWN_ERROR",
        "message": "Erreur Inconnue"
    }

def getErrorMessage(code):
    return getError(code)["message"]