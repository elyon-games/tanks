import pygame
from client.lib.screen.base import Screen

class gameEndScreen(Screen):
    def __init__(self, window):
        super().__init__(window, "game-end", "Fin de Jeu")

    def UpdateView(self):
        pass
