import pygame

keys = None

def getKeys() -> dict:
    global keys
    return keys

def updateKeys(keysSet) -> None:
    global keys
    keys = keysSet
