from pygame.font import SysFont, Font
from typing import Literal

fonts = {
    "titre": SysFont(None, 36),
    "texte": SysFont(None, 14),
    "hud_info": SysFont(None, 16),
    "username": SysFont(None, 30),
    "medium": SysFont(None, 24),
    "small": SysFont(None, 12),
    "big": SysFont(None, 48),
    "tiny": SysFont(None, 8)
}

def getFont(name: Literal["titre", "texte", "hud_info", "username", "medium", "small", "big", "tiny"]) -> Font:
    return fonts[name]

def getFontSize(size: int) -> Font:
    return Font(None, size)