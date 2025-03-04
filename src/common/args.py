import sys
from typing import Dict, Optional

return_args: Dict[str, str] = {}

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

def asArg(key: str) -> Optional[str]:
    return return_args.get(key)

def getArg(key: str) -> str:
    return return_args[key]

def getArgs() -> Dict[str, str]:
    return return_args