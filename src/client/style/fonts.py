from pygame.font import SysFont, Font

fonts = {
    "titre": SysFont(None, 36),
    "texte": SysFont(None, 14),
    "hud_info": SysFont(None, 16),
    "medium": SysFont(None, 24),
    "small": SysFont(None, 12),
    "big": SysFont(None, 48),
    "tiny": SysFont(None, 8)
}

def getFont(name) -> Font:
    return fonts[name]

def getFontSize(size) -> Font:
    return Font(None, size)