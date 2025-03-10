import pygame
from client.lib.screen.base import Screen
from client.lib.me import getData
from client.composants import NavBar
from client.style.fonts import getFontSize

class shopScreen(Screen):
    def __init__(self, window):
        super().__init__(window, "shop", "Boutique")
        self.user = getData().get("user")
        self.navbar = NavBar(window, self.user)

    def UpdateView(self):
        self.surface.blit(self.navbar.render(), (0, 0))
    
    def render_label(self, text, rect): 
        label_surface = getFontSize(30).render(text, True, (255, 255, 255))
        self.surface.blit(label_surface, (rect.x, rect.y))

    def HandleEvent(self, type, event):
        self.navbar.HandleEvent(type, event)
