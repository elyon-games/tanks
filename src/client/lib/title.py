import pygame
from common.utils import getDevModeStatus

global username
username = None

def setUsername(usernameSet) -> None:
    global username
    username = usernameSet

def changeTitle(title) -> None:
    dev_mode = getDevModeStatus()
    dev_suffix = " {Développement}" if dev_mode else ""
    
    if username:
        pygame.display.set_caption(f"Elyon Client{dev_suffix} ({username}) - {title}")
    else:
        pygame.display.set_caption(f"Elyon Client{dev_suffix} - {title}")
