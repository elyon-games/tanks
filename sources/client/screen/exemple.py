import pygame
from client.lib.screen.base import Screen

class exempleScreen(Screen):
    def __init__(self, window):
        super().__init__(window, "exemple", "Exemple")

    def UpdateView(self):
        pass
