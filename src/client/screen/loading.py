import pygame
from client.lib.screen.base import Screen
from client.types import EVENTS, KEYS
from client.style.fonts import getFontSize
from client.lib.title import changeTitle
from client.style.gradient import draw_gradient
from client.style.loader import draw_loader
from client.style.constants import EMERAUDE, BLEU, WHITE

class loadingScreen(Screen):
    def __init__(self, window):
        super().__init__(window, "loading", "Chargement...")
        self.angle = 0

    def UpdateView(self):
        draw_gradient(self.surface, EMERAUDE, BLEU, self.surface.get_width(), self.surface.get_height())
        center = (self.surface.get_width() // 2, self.surface.get_height() // 2)
        draw_loader(self.angle, self.surface, center, 50, WHITE)
        self.angle = (self.angle + 3.5) % 360
