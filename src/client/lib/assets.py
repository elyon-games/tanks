import pygame
import common.ams as AssetsManagerSystem
from typing import Dict, Union, Optional

assets: Dict[str, Dict[str, Union[pygame.Surface, pygame.mixer.Sound, str]]] = {}

def loadAsset(id: str, pathFile: str, type: str = "image") -> Union[pygame.Surface, pygame.mixer.Sound, Dict[str, Union[bool, str]]]:
    if type == "image":
        assets[id] = {
            "data": pygame.image.load(AssetsManagerSystem.getAsset(pathFile)),
            "type": type
        }
        return assets[id]["data"]
    elif type == "sound":
        assets[id] = {
            "data": pygame.mixer.Sound(AssetsManagerSystem.getAsset(pathFile)),
            "type": type
        }
        return assets[id]["data"]
    else:
        return {
            "status": False,
            "error": True,
            "message": "INVALID_TYPE"
        }

def getAsset(id: str) -> Optional[Union[pygame.Surface, pygame.mixer.Sound]]:
    return assets[id]["data"] if id in assets else None

def getAssetType(id: str) -> Optional[str]:
    return assets[id]["type"] if id in assets else None

def getAssets() -> Dict[str, Dict[str, Union[pygame.Surface, pygame.mixer.Sound, str]]]:
    return assets