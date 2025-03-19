from client.lib.storage.controller import getStorage

# Initialisation du dictionnaire des contrôles
default_controls = {
    "up_key": "z",
    "down_key": "s",
    "left_key": "q",
    "right_key": "d",
    "shoot_key": "space"
}

commonStorage = getStorage("common")
stored_controls = commonStorage.getKey("controls") or {}

# Compléter les contrôles manquants avec les valeurs par défaut
controls = {**default_controls, **stored_controls}

# Sauvegarder les contrôles mis à jour dans le stockage commun
commonStorage.addData("controls", controls)
commonStorage.saveData()

# Fonction pour récupérer les contrôles
def get_controls():
    global controls
    return controls

# Fonction pour définir un contrôle
def set_control(key: str, value: str):
    global controls
    controls[key] = value
    commonStorage.addData("controls", controls)
    commonStorage.saveData()

# Fonction pour récupérer un contrôle
def get_control(key: str):
    global controls
    return controls[key]