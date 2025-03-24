import sys
from typing import Dict, Optional

return_args: Dict[str, str] = {}

# fonction pour formater les arguments de la ligne de commande
def get_format_args() -> Dict[str, str]:
    global return_args
    args = sys.argv[1:]
    current_key: Optional[str] = None

    for arg in args:
        if arg.startswith("--"):
            current_key = arg[2:]
        elif current_key:
            return_args[current_key] = arg
            current_key = None

    return return_args

# fonction pour savoir si un argument est présent dans les arguments de la ligne de commande
def asArg(key: str) -> Optional[str]:
    return return_args.get(key)

# fonction pour récupérer un argument des arguments de la ligne de commande
def getArg(key: str) -> str:
    return return_args[key]

# fonction pour récupérer tous les arguments de la ligne de commande
def getArgs() -> Dict[str, str]:
    return return_args