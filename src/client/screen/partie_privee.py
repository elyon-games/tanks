import pygame
from client.lib.screen.base import Screen
from client.lib.me import getData
from client.composants import NavBar
from client.style.fonts import getFont
from client.style.constants import EMERAUDE, BLACK, GRAY, BLEU
from client.style.fonts import getFontSize
from client.lib.utils import getMaps
from client.style.constants import EMERAUDE, BLEU, WHITE, BLACK, GRAY, STEEL_BLUE, LIGHTER_BLUE, CARD_COLOR, CARD_BORDER_COLOR


class privatePartieScreen(Screen):
    def __init__(self, window):
        super().__init__(window, "private-party", "Partie Privée")
        self.user = getData().get("user")
        self.maps: list[dict] = getMaps()
        self.navbar = NavBar(window, self.user)
        self.show_modal = False
        self.is_private = False
        self.selected_map = None
        self.create_button = pygame.Rect(50, 50, 200, 50)
        self.map_buttons = []
        self.dropdown_open = False
        self.id_partie = ""
        self.partie_is_create = False

    def render_label(self, text, rect, size=30, color=(255, 255, 255)): 
        label_surface = getFontSize(size).render(text, True, color)
        self.window.blit(label_surface, (rect.x, rect.y))
    
    def render_text_input(self, rect, text):
        border_color = (255,255,255)
        self.draw_rounded_rect(self.surface, rect, BLACK, border_radius=10)
        pygame.draw.rect(self.surface, border_color, rect, 2, border_radius=10)
        text_surface = getFontSize(32).render(text, True, (255,255,255))
        self.surface.blit(text_surface, (rect.x + 10, rect.y + 8))
    
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
    
    def render_button(self, rect, text):
        color = LIGHTER_BLUE 
        self.draw_rounded_rect(self.surface, rect, color, border_radius=10)
        text_surface = getFontSize(32).render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=rect.center)
        self.surface.blit(text_surface, text_rect)
    
    def handle_paste(self):
        try:
            clipboard_text = pygame.scrap.get(pygame.SCRAP_TEXT).decode("utf-8")
            self.id_partie += clipboard_text
        except Exception as e:
            print(f"Erreur lors du collage : {e}")
    
    def UpdateView(self):
        self.id_partie = self.id_partie.replace("\x00", "").strip()
        self.surface.blit(self.navbar.render(), (0, 0))
        
        label_rect = pygame.Rect(self.window.get_width()/2-275, self.window.get_height()/3 - 60, 550, 60)
        self.render_label("Rejoindre une partie privée", label_rect, 60)
        
        self.id_partie_rect = pygame.Rect(self.window.get_width()/2 - 150, self.window.get_height()/3, 300, 40)
        self.render_text_input(self.id_partie_rect, self.id_partie)
        
        self.login_button_rect = pygame.Rect(self.window.get_width()/2+25, self.window.get_height()/2, 150, 40)
        self.render_button(self.login_button_rect, "Rejoindre")
        
        self.create_party_rect = pygame.Rect(self.window.get_width()/2-175, self.window.get_height()/2, 150, 40)
        self.render_button(self.create_party_rect, "Créer")
        
        
        

    def HandleEvent(self, type, event):
        self.UpdateView()
        if type == pygame.MOUSEBUTTONDOWN:
            if self.create_party_rect.collidepoint(event.pos):
                self.partie_is_create = True
                self.id_partie = "123456"
                
        elif type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.id_partie = self.id_partie[:-1]
            elif event.key == pygame.K_v and (self.keys[pygame.K_LCTRL] or self.keys[pygame.K_RCTRL]):
                self.handle_paste()
            elif len(self.id_partie) < 20:
                self.id_partie += event.unicode
        self.navbar.HandleEvent(type, event)
