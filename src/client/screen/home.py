import pygame
from client.lib.screen.base import Screen
from client.lib.me import getData
from client.composants import NavBar
from client.style.fonts import getFont
from client.style.constants import EMERAUDE, BLACK, GRAY, BLEU
from client.style.fonts import getFontSize
import webbrowser


class HomeScreen(Screen):
    def __init__(self, window):
        super().__init__(window, "home", "Accueil")
        self.user = getData().get("user")
        self.navbar = NavBar(window, self.user)

    def render_label(self, text, rect, size=30, color=(255, 255, 255)): 
        label_surface = getFontSize(size).render(text, True, color)
        self.window.blit(label_surface, (rect.x, rect.y))
    
    def UpdateView(self):
        title_rect = pygame.Rect((self.window.get_width() - (self.window.get_width()-180-500))//2, self.window.get_height()*0.2, 500, 100)
        pygame.draw.rect(self.window, (0,0,0), title_rect)
        self.render_label("Bienvenue sur Elyon Tanks", title_rect, 60)
        
        
        
        self.link_to_doc = pygame.Rect(15, self.window.get_height()-40, 150, 30)
        self.render_label("Documentation", self.link_to_doc, color=(0,0,246))
        self.surface.blit(self.navbar.render(), (0, 0))

    def HandleEvent(self, type, event):
        self.UpdateView()
        if self.link_to_doc.collidepoint(pygame.mouse.get_pos()):
            if type == pygame.MOUSEBUTTONDOWN:
                webbrowser.open("https://elyon.younity-mc.fr/documentation")
        self.navbar.HandleEvent(type, event)