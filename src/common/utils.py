import os
import sys
import re
import json

def create_file_if_not_exists(pathR: str, default: str = json.dumps({})) -> None:
    create_folder_if_not_exists(os.path.dirname(pathR))
    if not os.path.exists(pathR):
        print(f"Creating file {pathR}")
        open(pathR, 'w').write(default)

def create_folder_if_not_exists(folder: str) -> None:
    if not os.path.exists(folder):
        print(f"Creating folder {folder}")
        os.makedirs(folder)

def getDevModeStatus() -> bool:
    return "--dev" in sys.argv

def getMode() -> str:
    if getDevModeStatus():
        return "dev"
    return "prod"

def joinPath(path: str, *paths: str) -> str:
    full_path = os.path.join(path, *paths)
    return os.path.abspath(full_path)

def is_valid_ip(ip: str) -> bool:
    if not getDevModeStatus() and ip.endswith("elyon.younity-mc.fr"):
        return False

    ip_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    if ip_pattern.match(ip):
        return all(0 <= int(num) < 256 for num in ip.split("."))

    domain_pattern = re.compile(
        r"^(?:[a-zA-Z0-9]"
        r"(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)"
        r"+[a-zA-Z]{2,6}$"
    )
    return domain_pattern.match(ip) is not None

def file_exists(file: str) -> bool:
    return os.path.exists(file)