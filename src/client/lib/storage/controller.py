from client.lib.storage.base import File
from typing import Optional

storages: dict[str, File] = {}

def createStorage(id: str, path: str, default: Optional[dict] = None) -> File:
    if id not in storages:
        storages[id] = File(id, path, default)
    return storages[id]

def getStorage(id) -> Optional[File]:
    if id in storages:
        return storages[id]
    return None