import pygame
from client.lib.screen.base import Screen

class gameScreen(Screen):
    def __init__(self, window):
        super().__init__(window, "game", "Jeu")

    def UpdateView(self):
        pass
