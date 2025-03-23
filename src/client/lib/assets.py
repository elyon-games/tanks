import pygame
import common.ams as AssetsManagerSystem
from typing import Dict, Union, Optional

# Assets Manager System Client (AMS-CLIENT)

assets: Dict[str, Dict[str, Union[pygame.Surface, pygame.mixer.Sound, str]]] = {}

# Fonction pour charger un assets
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

# Fonction pour récupérer un assets et le redimensionner si besoin
def getAsset(id: str, size: Union[float, tuple] = 1) -> Optional[Union[pygame.Surface, pygame.mixer.Sound]]:
    A = assets[id]["data"] if id in assets else None
    if isinstance(size, tuple):
        A = pygame.transform.scale(A, size)
    elif size != 1:
        A = pygame.transform.scale_by(A, size)
    return A

# Fonction pour récupérer le type d'un assets
def getAssetType(id: str) -> Optional[str]:
    return assets[id]["type"] if id in assets else None

# Fonction pour récupérer tous les assets
def getAssets() -> Dict[str, Dict[str, Union[pygame.Surface, pygame.mixer.Sound, str]]]:
    return assets