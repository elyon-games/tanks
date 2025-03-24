import pygame
from client.lib.screen.base import Screen

class gameWaitScreen(Screen):
    def __init__(self, window):
        super().__init__(window, "game-wait", "Attente de Partie")

    def UpdateView(self):
        pass
