import pygame
from client.lib.screen.base import Screen
from client.lib.me import getData
from client.composants import NavBar
from client.style.fonts import getFont
from client.style.constants import EMERAUDE, BLACK, GRAY, BLEU

class HomeScreen(Screen):
    def __init__(self, window):
        super().__init__(window, "home", "Accueil")
        self.user = getData().get("user")
        self.navbar = NavBar(window, self.user)

    def UpdateView(self):
        self.surface.blit(self.navbar.render(), (0, 0))

    def HandleEvent(self, type, event):
        self.navbar.HandleEvent(type, event)