import pygame
from client.lib.screen.base import Screen

class gameMainScreen(Screen):
    def __init__(self, window):
        super().__init__(window, "game-main", "Jeu")

    def UpdateView(self):
        pass
