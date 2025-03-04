import pygame
from client.lib.screen.base import Screen
from client.composants import NavBar
from client.lib.me import getData

class settingsScreen(Screen):
    def __init__(self, window):
        super().__init__(window, "settings", "Paramètres")
        self.user = getData().get("user")
        self.navbar = NavBar(window, self.user)

    def UpdateView(self):
        self.surface.blit(self.navbar.render(), (0, 0))

    def HandleEvent(self, type, event):
        self.navbar.HandleEvent(type, event)
