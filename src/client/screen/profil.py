import pygame
from client.lib.screen.base import Screen
from client.lib.me import getData
from client.composants import NavBar, showUsername
from client.lib.screen.controller import getArgs
from client.style.fonts import getFont
from client.lib.utils import getProfil
from client.style.constants import EMERAUDE
from client.lib.title import changeTitle

class profilScreen(Screen):
    def __init__(self, window):
        super().__init__(window, "profil", "Profil")
        self.user = getData().get("user")
        self.navbar = NavBar(window, self.user)
        self.profilID = getArgs("show_profil_id")
        self.user = getProfil(self.profilID)
        changeTitle(f"Profil | {str(self.user['username'])}")

    def UpdateView(self):
        self.surface.blit(self.navbar.render(), (0, 0))
        self.renderProfileDetails()

    def renderProfileDetails(self):
        y_offset = 100
        padding = 20
        card_width = 600
        card_height = 300
        card_rect = pygame.Rect((self.surface.get_width() - card_width) // 2, y_offset, card_width, card_height)
        pygame.draw.rect(self.surface, (50, 50, 50), card_rect)
        pygame.draw.rect(self.surface, (255, 255, 255), card_rect, 2)

        username_display = showUsername(self.window, self.user["username"], self.user["rank"], EMERAUDE, 50)
        self.surface.blit(username_display.render(), (card_rect.x + padding, card_rect.y + padding))

        

    def HandleEvent(self, type, event):
        self.navbar.HandleEvent(type, event)