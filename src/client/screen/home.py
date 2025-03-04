import pygame
from client.lib.screen.base import Screen
from client.lib.me import getData
from client.var import auth as authData
from client.style.constants import EMERAUDE, BLACK
import client.lib.notifications.controller as notifications
from client.style.gradient import draw_gradient
from client.lib.assets import getAsset

# from client.composants.input import Input

class HomeScreen(Screen):
    def __init__(self, window):
        super().__init__(window, "home", "Accueil")
        self.logo = getAsset("logo")
    
    def UpdateView(self):
        draw_gradient(self.surface, EMERAUDE, BLACK, *self.getSize())
        self.test_button = pygame.Rect(50, 50, 200, 50)
        pygame.draw.rect(self.surface, (0, 128, 255), self.test_button)
        font = pygame.font.Font(None, 36)
        text = font.render('Test Button', True, (255, 255, 255))
        text_rect = text.get_rect(center=self.test_button.center)
        self.surface.blit(text, text_rect)
        self.surface.blit(self.logo, (0, 0))

    def HandleEvent(self, type, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.test_button.collidepoint(event.pos):
                notifications.showNotification("Button clicked", 5)
