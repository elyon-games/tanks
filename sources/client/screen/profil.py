import pygame
from client.lib.screen.base import Screen
from client.lib.me import getData
from client.composants import NavBar, showUsername
from client.lib.screen.controller import getArgs
from client.style.fonts import getFont
from client.lib.utils import getProfil
from client.style.constants import EMERAUDE
from client.lib.title import changeTitle
from client.style.fonts import getFontSize

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

    def render_label(self, text, rect): 
        label_surface = getFontSize(30).render(text, True, (255, 255, 255))
        self.surface.blit(label_surface, (rect.x, rect.y))

    def renderProfileDetails(self):
        y_offset = 100
        padding = 20
        card_width = self.window.get_width()*0.8
        card_height = self.window.get_height()*0.8
        card_rect = pygame.Rect((self.window.get_width() - card_width)/2, y_offset, card_width, card_height)
        pygame.draw.rect(self.surface, (50, 50, 50), card_rect)
        pygame.draw.rect(self.surface, (255, 255, 255), card_rect, 2)
        username_display = showUsername(self.window, self.user["username"], self.user["rank"], EMERAUDE, 50)
        self.surface.blit(username_display.render(), (card_rect.x + padding, card_rect.y + padding))

        if self.user["admin"]:
            adm_rect = pygame.Rect(card_rect.x + padding + 20, card_rect.y + padding + 50, 100, 30)
            self.render_label("Administrateur : True", adm_rect)

        date_rect = pygame.Rect(card_rect.x + padding + 20, card_rect.y + padding + 100, 100, 30)
        self.render_label(f"Date de création : {self.user['created_at'][0:10]}", date_rect)

        text_rect = pygame.Rect(card_width - padding - 40 -150, card_rect.y + padding + 50, 100, 30)
        self.render_label(f"Statistique : ", text_rect)

        y = 0
        for stat_key, stat_value in self.user["stats"].items():
            rect = pygame.Rect(card_width - padding - 40 -110, card_rect.y + padding + 100 + y, 100, 30)
            self.render_label(f"- {stat_key} : {stat_value}", rect)
            y+=40 

        

    def HandleEvent(self, type, event):
        self.navbar.HandleEvent(type, event)