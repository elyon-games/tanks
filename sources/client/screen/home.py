import pygame
from client.lib.screen.base import Screen
from client.lib.me import getData
from client.composants import NavBar
from client.style.fonts import getFont
from client.style.constants import EMERAUDE, BLEU, WHITE, BLACK, GRAY, STEEL_BLUE, LIGHTER_BLUE, CARD_COLOR, CARD_BORDER_COLOR
from client.style.fonts import getFontSize
import webbrowser
from client.lib.maps import getMaps
from client.lib.screen.controller import showScreen
from client.lib.parties import getPartysPublicShow, joinParty
class HomeScreen(Screen):
    def __init__(self, window):
        super().__init__(window, "home", "Accueil")
        self.user = getData().get("user")
        self.maps: list[dict] = getMaps()
        self.navbar = NavBar(window, self.user)
        self.show_modal = False
        self.is_private = False
        self.selected_map = None
        self.create_button = pygame.Rect(50, 50, 200, 50)
        self.party_public_show = getPartysPublicShow()
        self.map_buttons = []
        self.dropdown_open = False

    def render_label(self, text, rect, size=30, color=(255, 255, 255)): 
        label_surface = getFontSize(size).render(text, True, color)
        self.window.blit(label_surface, (rect.x, rect.y))
    
    def render_button(self, rect, text):
        color = LIGHTER_BLUE
        self.draw_rounded_rect(self.surface, rect, color, border_radius=10)
        text_surface = getFontSize(32).render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=rect.center)
        self.surface.blit(text_surface, text_rect)
    
    def draw_rounded_rect(self, surface, rect, color, border_radius=20, border_color=None, border_width=0):
        x, y, w, h = rect
        pygame.draw.rect(surface, color, (x + border_radius, y, w - 2 * border_radius, h))  # Centre
        pygame.draw.rect(surface, color, (x, y + border_radius, w, h - 2 * border_radius))  # Verticales
        pygame.draw.circle(surface, color, (x + border_radius, y + border_radius), border_radius)  # Coin haut gauche
        pygame.draw.circle(surface, color, (x + w - border_radius, y + border_radius), border_radius)  # Coin haut droit
        pygame.draw.circle(surface, color, (x + border_radius, y + h - border_radius), border_radius)  # Coin bas gauche
        pygame.draw.circle(surface, color, (x + w - border_radius, y + h - border_radius), border_radius)  # Coin bas droit

        if border_width > 0 and border_color:
            inner_rect = pygame.Rect(
                x + border_width, y + border_width, w - 2 * border_width, h - 2 * border_width
            )
            self.draw_rounded_rect(surface, inner_rect, border_color, border_radius - border_width)
    
    def UpdateView(self):
        self.surface.blit(self.navbar.render(), (0, 0))
        title_rect = pygame.Rect((self.window.get_width())//3 - 180, self.window.get_height()*0.2, 550, 100)
        # pygame.draw.rect(self.window, (0,0,0), title_rect)
        self.render_label("Bienvenue sur Elyon Tanks", title_rect, 60)
        
        
        #partie privé 
        self.private_partie_rect = pygame.Rect(self.window.get_width() - 160, self.window.get_height()-60-60, 150, 50)
        self.render_button(self.private_partie_rect, "Partie privée")
        
        #bouton jouer
        self.join_classic_rect = pygame.Rect(self.window.get_width() - 160, self.window.get_height()-60, 150, 50)
        self.render_button(self.join_classic_rect, "Jouer")
        
        #lien vers la documentation
        self.link_to_doc = pygame.Rect(15, self.window.get_height()-40, 150, 30)
        self.render_label("Documentation", self.link_to_doc, color=(0,0,246))

    def HandleEvent(self, type, event):
        self.UpdateView()
        if type == pygame.MOUSEBUTTONDOWN:
            if self.link_to_doc.collidepoint(pygame.mouse.get_pos()):
                webbrowser.open("https://elyon.younity-mc.fr/documentation")
            if self.private_partie_rect.collidepoint(pygame.mouse.get_pos()):
                showScreen("private-party")
            if self.join_classic_rect.collidepoint(pygame.mouse.get_pos()):
                info = joinParty(private=False)
                print("Join Info", info)
                showScreen("game-main", {
                    "party_id": info["party_id"],
                })

        self.navbar.HandleEvent(type, event)
