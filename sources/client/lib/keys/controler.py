import pygame
keys = None

def getKeys() -> dict:
    global keys
    return keys

# Fonction pour mettre a jour les touches appuyées
# Cette fonction gère également le "backScreen" pour revenir au screen précédent avec la touche CTRL+Z
def updateKeys(keysSet) -> None:
    global keys
    keys = keysSet
    from client.lib.screen.controller import backScreen
    if keys[pygame.K_LCTRL] and keys[pygame.K_z]:
        backScreen()

