import datetime

# Fonction pour récupérer l'heure actuelle au format ISO
def get_current_time() -> str:
    return datetime.datetime.now().isoformat()

# Fonction pour récupérer l'année actuelle
def get_current_year() -> int:
    return int(datetime.datetime.now().year)