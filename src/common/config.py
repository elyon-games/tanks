import yaml
import os
import sys
from typing import Any, Dict, Optional
from common.utils import getMode

def resource_path(relative_path: str) -> str:
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

path_all_config: str = resource_path("config")

def openConfig(path: str) -> Optional[Dict[str, Any]]:
    try:
        with open(path, "r") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Erreur : Le fichier {path} est introuvable.")
        sys.exit(1)
    except yaml.YAMLError as exc:
        print(f"Erreur lors de l'analyse du fichier YAML {path} : {exc}")
        sys.exit(1)
    except Exception as exc:
        print(f"Une erreur inattendue s'est produite lors de l'ouverture de {path} : {exc}")
        sys.exit(1)

def ensure_config_exists() -> None:
    global path_all_config
    external_config_path = os.path.join(os.path.abspath("."), "config")
    if os.path.exists(external_config_path) and os.path.isdir(external_config_path):
        path_all_config = external_config_path
    else:
        print("Info : Le dossier 'config' n'a pas été trouvé à côté de l'exécutable.")
        print("Utilisation des fichiers de configuration embarqués.")
        path_all_config = resource_path("config")

ensure_config_exists()

try:
    common_config_path = os.path.join(path_all_config, "common.yaml")
    common_config: Dict[str, Any] = openConfig(common_config_path) or {}
except Exception as exc:
    common_config = {}
    print(f"Une erreur s'est produite lors du chargement de la configuration commune : {exc}")
    sys.exit(1)

app_configs: Dict[str, Dict[str, Any]] = {}

def initConfig(app: str, mode: str) -> None:
    global app_configs
    try:
        config_path = os.path.join(path_all_config, f"{app}.yaml")
        config = openConfig(config_path)
        if config is None:
            raise ValueError(f"La configuration pour {app} est vide ou invalide.")
        final_config = config[mode].copy()
        if config.get("all"):
            final_config.update(config["all"])
        final_config.update(common_config)
        app_configs[app] = final_config
    except KeyError:
        print(f"Erreur : La config '{mode}' n'existe pas dans la configuration pour {app}.")
        sys.exit(1)
    except ValueError as exc:
        print(exc)
        sys.exit(1)
    except Exception as exc:
        print(f"Une erreur inattendue s'est produite lors de l'initialisation de la configuration pour {app} : {exc}")
        sys.exit(1)

def setConfigParameter(app: str, key: str, value: Any) -> None:
    if app not in app_configs:
        initConfig(app, getMode())
    keys = key.split('.')
    d = app_configs[app]
    for k in keys[:-1]:
        if k not in d or not isinstance(d[k], dict):
            d[k] = {}
        d = d[k]
    d[keys[-1]] = value

def getConfig(app: str) -> Dict[str, Any]:
    if app not in app_configs:
        initConfig(app, getMode())
    return app_configs[app]
