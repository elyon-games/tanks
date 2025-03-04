import pygame
from client.lib.screen.base import Screen

class AuthRegisterScreen(Screen):
    def __init__(self, window):
        super().__init__(window, "register", "S'inscrire")

    def UpdateView(self):
        pass
