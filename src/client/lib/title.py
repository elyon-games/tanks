import pygame
from common.utils import getDevModeStatus

global username
username = None

# Fonction pour définir le nom d'utilisateur dans le titre de la fenêtre
def setUsername(usernameSet) -> None:
    global username
    username = usernameSet

# Fonction pour changer le titre de la fenêtre
def changeTitle(title) -> None:
    dev_mode = getDevModeStatus() # Récupération du mode de développement
    dev_suffix = " {Développement}" if dev_mode else "" # Ajout du suffixe de développement si le mode de développement est activé
    
    # Changement du titre de la fenêtre avec ou non le nom d'utilisateur
    if username:
        pygame.display.set_caption(f"Elyon Client{dev_suffix} ({username}) - {title}")
    else:
        pygame.display.set_caption(f"Elyon Client{dev_suffix} - {title}")
