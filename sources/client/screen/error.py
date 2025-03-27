import pygame
from client.lib.screen.base import Screen
from client.types import WINDOW
from client.style.gradient import draw_gradient
from client.style.constants import EMERAUDE, RED

class errorScreen(Screen):
    def __init__(self, window: WINDOW, message: str):
        super().__init__(window, "error", "Erreur")
        self.message = message

    def UpdateView(self):
        draw_gradient(self.surface, EMERAUDE, RED, *self.getSize())
        pass