from typing import Dict

import common.ams
from common.utils import joinPath

global path_data
global paths

path_data: str = None
paths: Dict[str, str] = {}

# fonction pour initialiser les chemins de fichiers et dossiers 
def initPath(path_data_t: str = "./data") -> None:
    global path_data
    global paths
    path_data = path_data_t
    print("Path Data : ", path_data)
    paths = {
        # main code
        "src": "./sources",
        "common": "./sources/common",
        # data
        "data": path_data,
        # interne
        "config": "./config",
        "assets": common.ams.getAsset("./assets"),
        # logs
        "logs": joinPath(path_data, "logs"),
        # client
        "client": "./sources/client",
        "client_data": joinPath(path_data, "client"),
        "client_data_servers": joinPath(path_data, "client", "servers"),
        # server
        "server": "./sources/server",
        "server_public": "./sources/server/routes/web/static",
        "server_templates": "./sources/server/routes/web/templates",
        "server_data": joinPath(path_data, "server"),
        "server_database": joinPath(path_data, "server/database"),
        "server_files": joinPath(path_data, "server/files"),
        "server_sessions": joinPath(path_data, "server/sessions")
    }

# fonction pour récupérer un chemin de fichier ou de dossier 
def get_path(key: str = "default") -> str:
    return joinPath(paths.get(key, "./"))
