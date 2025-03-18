import pygame
from client.lib.screen.base import Screen
from client.lib.me import getData
from client.composants import NavBar
from client.style.fonts import getFont
from client.style.constants import EMERAUDE, BLACK, GRAY, BLEU
from client.style.fonts import getFontSize

class HomeScreen(Screen):
    def __init__(self, window):
        super().__init__(window, "home", "Accueil")
        self.user = getData().get("user")
        self.navbar = NavBar(window, self.user)

    def render_label(self, text, rect, size=30): 
        label_surface = getFontSize(size).render(text, True, (255, 255, 255))
        self.window.blit(label_surface, (rect.x, rect.y))
    
    def UpdateView(self):
        title_rect = pygame.Rect(self.window.get_width()/2 - 250, self.window.get_height()*0.2, 300, 100)
        self.render_label("Bienvenue sur Elyon Tanks", title_rect, 60)
        
        
        
        self.surface.blit(self.navbar.render(), (0, 0))

    def HandleEvent(self, type, event):
        self.navbar.HandleEvent(type, event)