import pygame
from client.style.gradient import draw_gradient
from client.lib.me import getData
from client.style.fonts import getFont
from client.style.constants import EMERAUDE, BLACK, GRAY, BLEU, WHITE
from client.lib.screen.controller import showScreen
from client.style.gradient import draw_gradient
from client.lib.assets import getAsset
from client.lib.auth import logout

class composantBase():
    def __init__(self, window):
        self.window = window
        self.updateSurface()
        
    
    def updateSurface(self):
        self.surface = pygame.surface.Surface(self.getSize())

    def getSize(self):
        return self.window.get_size()

class NavBar(composantBase):
    def __init__(self, window, user):
        super().__init__(window)
        self.logo = getAsset("logo", 0.35)
        self.user = user
        self.font = getFont("medium")
        self.fontTitre = getFont("titre")
        self.menu_open = False
        self.menu_animation_progress = 0
        self.buttons = [
            {
                "text": "Boutique",
                "screen": "shop"
            }
        ]

    def render(self):
        self.updateSurface() # IMPORTANT
        draw_gradient(self.surface, EMERAUDE, BLACK, *self.getSize())
        self.logoPos = self.surface.blit(self.logo, (20, 10))
        self.surface.blit(self.fontTitre.render("Elyon Tanks", False, BLACK), (self.logoPos.x*5, self.logoPos.centery-10))
        self.draw_buttons()
        self.draw_user_card()
        return self.surface # IMPORTANT

    def draw_buttons(self):
        i=0
        for button in self.buttons:
            i+=1
            self.surface.blit(self.font.render(f"{button.get("text", "")}", False, BLACK), (self.logoPos.x*(12+i), 
                                                                                            self.logoPos.centery-4))
        

    def draw_text(self, text, position):
            text_surface = self.font.render(text, True, EMERAUDE)
            self.surface.blit(text_surface, position)

    def draw_user_card(self):
        window_width = self.surface.get_width()
        user_card_rect = pygame.Rect(window_width - 200, 20, 180, 50)
        pygame.draw.rect(self.surface, GRAY, user_card_rect, border_radius=10)
        
        username_surface = self.font.render(self.user['username'], True, BLACK)
        username_rect = username_surface.get_rect(center=user_card_rect.center)
        
        self.surface.blit(username_surface, username_rect.topleft)
        
        if self.menu_open:
            self.draw_user_menu(user_card_rect)

    def draw_user_menu(self, user_card_rect):
        menu_items = ["Voir mon profil", "Paramètres", "Déconnexion"]
        menu_height = len(menu_items) * 30 + 20
        menu_rect = pygame.Rect(user_card_rect.left, user_card_rect.bottom + 10, 180, menu_height)
        
        # Animation effect
        if self.menu_animation_progress < 1:
            self.menu_animation_progress += 0.1
        animated_height = int(menu_height * self.menu_animation_progress)
        animated_rect = pygame.Rect(menu_rect.left, menu_rect.top, menu_rect.width, animated_height)
        
        pygame.draw.rect(self.surface, BLEU, animated_rect, border_radius=10)
        
        for index, item in enumerate(menu_items):
            item_surface = self.font.render(item, True, pygame.Color('white'))
            item_rect = item_surface.get_rect(center=(menu_rect.centerx, menu_rect.top + 20 + index * 30))
            self.surface.blit(item_surface, item_rect.topleft)

    def HandleEvent(self, type, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            user_card_rect = pygame.Rect(self.surface.get_width() - 200, 20, 180, 50)
            if self.logo.get_rect().collidepoint(mouse_pos):
                showScreen("home")
            if user_card_rect.collidepoint(mouse_pos):
                self.menu_open = not self.menu_open
                self.menu_animation_progress = 0
            if self.menu_open:
                profile_rect = pygame.Rect(user_card_rect.left + 10, user_card_rect.bottom + 10, 180, 30)
                settings_rect = pygame.Rect(user_card_rect.left + 10, user_card_rect.bottom + 40, 180, 30)
                logout_rect = pygame.Rect(user_card_rect.left + 10, user_card_rect.bottom + 70, 180, 30)
                if profile_rect.collidepoint(mouse_pos):
                    showScreen("profil")
                elif settings_rect.collidepoint(mouse_pos):
                    showScreen("settings")
                elif logout_rect.collidepoint(mouse_pos):
                    logout()