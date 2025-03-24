import os
import sys

# AMS: Asset Management System
# Ce module permet de gérer les assets (images, sons, etc.) de l'application

# fonction pour récupérer le chemin d'un asset
def getAsset(relative_path: str) -> str:
    cleaned_path = relative_path.lstrip("/").replace("/", os.sep)
    base_path = os.path.join(sys._MEIPASS, "assets") if hasattr(sys, "_MEIPASS") else os.path.join(os.path.abspath("."), "assets")
    return os.path.join(base_path, cleaned_path)

# fonction pour récupérer le contenu d'un asset
def getAssetContent(relative_path: str) -> str:
    return open(getAsset(relative_path), "r").read()


# fonction pour récupérer le contenu d'un asset en tant que bytes
def getAllAssetsIn(path: str) -> list:
    assets = []
    for root, dirs, files in os.walk(getAsset(path)):
        for file in files:
            assets.append(os.path.join(root, file))
    return assets