import pygame
keys = None

def getKeys() -> dict:
    global keys
    return keys

def updateKeys(keysSet) -> None:
    global keys
    keys = keysSet
    from client.lib.screen.controller import backScreen
    if keys[pygame.K_LCTRL] and keys[pygame.K_z]:
        backScreen()

