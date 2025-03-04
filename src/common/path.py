from typing import Dict

import common.ams
from common.utils import joinPath

global path_data
global paths

path_data: str = None
paths: Dict[str, str] = {}

def initPath(path_data_t: str = "./data") -> None:
    global path_data
    global paths
    path_data = path_data_t
    print("Path Data : ", path_data)
    paths = {
        # main code
        "src": "./src",
        "common": "./src/common",
        # data
        "data": path_data,
        # interne
        "config": "./config",
        "assets": common.ams.getAsset("./assets"),
        # logs
        "logs": joinPath(path_data, "logs"),
        # client
        "client": "./src/client",
        "client_data": joinPath(path_data, "client"),
        "client_data_servers": joinPath(path_data, "client", "servers"),
        # server
        "server": "./src/server",
        "server_public": "./src/server/public",
        "server_templates": "./src/server/templates",
        "server_data": joinPath(path_data, "server"),
        "server_database": joinPath(path_data, "server/database"),
        "server_files": joinPath(path_data, "server/files"),
        "server_sessions": joinPath(path_data, "server/sessions")
    }
    
def get_path(key: str = "default") -> str:
    return joinPath(paths.get(key, "./"))
