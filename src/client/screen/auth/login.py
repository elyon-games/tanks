import pygame
from client.style.gradient import draw_gradient
from client.style.constants import EMERAUDE, BLEU, WHITE, BLACK, GRAY, STEEL_BLUE, LIGHTER_BLUE, CARD_COLOR, CARD_BORDER_COLOR
from client.style.fonts import getFontSize
from client.lib.screen.base import Screen
from client.types import EVENTS, KEYS
from client.lib.title import changeTitle
from client.lib.auth import login
from client.lib.screen.controller import showScreen

class AuthLoginScreen(Screen):
    def __init__(self, window):
        super().__init__(window, "auth-login", "Authentification - Connexion")
        self.email = ""
        self.password = ""
        self.active_input = None

    def draw_rounded_rect(self, surface, rect, color, border_radius=20, border_color=None, border_width=0):
        """Dessine un rectangle avec des coins arrondis."""
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

    def render_text_input(self, rect, text, active):
        border_color = WHITE if active else GRAY
        self.draw_rounded_rect(self.surface, rect, BLACK, border_radius=10)
        pygame.draw.rect(self.surface, border_color, rect, 2, border_radius=10)
        text_surface = getFontSize(32).render(text, True, WHITE)
        self.surface.blit(text_surface, (rect.x + 10, rect.y + 8))

    def render_button(self, rect, text, hover):
        color = LIGHTER_BLUE if hover else STEEL_BLUE
        self.draw_rounded_rect(self.surface, rect, color, border_radius=10)
        text_surface = getFontSize(32).render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=rect.center)
        self.surface.blit(text_surface, text_rect)

    def handle_paste(self):
        try:
            clipboard_text = pygame.scrap.get(pygame.SCRAP_TEXT).decode('utf-8')
            if self.active_input == "email":
                self.email += clipboard_text
            elif self.active_input == "password":
                self.password += clipboard_text
        except Exception as e:
            print(f"Erreur lors du collage: {e}")

    def UpdateView(self):
        # Background
        draw_gradient(self.surface, EMERAUDE, BLEU, self.surface.get_width(), self.surface.get_height())

        # Center card dimensions
        card_width, card_height = 400, 300
        card_x = (self.surface.get_width() - card_width) // 2
        card_y = (self.surface.get_height() - card_height) // 2

        # Draw card with rounded corners
        self.draw_rounded_rect(self.surface, (card_x, card_y, card_width, card_height), CARD_COLOR, border_radius=20, border_color=CARD_BORDER_COLOR, border_width=2)

        # Input fields
        email_rect = pygame.Rect(card_x + 50, card_y + 50, 300, 40)
        password_rect = pygame.Rect(card_x + 50, card_y + 110, 300, 40)
        self.render_text_input(email_rect, self.email, self.active_input == "email")
        self.render_text_input(password_rect, "*" * len(self.password), self.active_input == "password")

        # Button
        button_rect = pygame.Rect(card_x + 150, card_y + 200, 100, 40)
        mouse_pos = pygame.mouse.get_pos()
        button_hover = button_rect.collidepoint(mouse_pos)
        self.render_button(button_rect, "Login", button_hover)

        for event in self.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if email_rect.collidepoint(event.pos):
                    self.active_input = "email"
                elif password_rect.collidepoint(event.pos):
                    self.active_input = "password"
                elif button_rect.collidepoint(event.pos):
                    self.active_input = None
                    if login(self.email, self.password) == True:
                        showScreen("home")
                    else:
                        self.password = ""
                else:
                    self.active_input = None
            elif event.type == pygame.KEYDOWN and self.active_input:
                if event.key == pygame.K_BACKSPACE:
                    if self.active_input == "email":
                        self.email = self.email[:-1]
                    elif self.active_input == "password":
                        self.password = self.password[:-1]
                elif event.key == pygame.K_v and (self.keys[pygame.K_LCTRL] or self.keys[pygame.K_RCTRL]):
                    self.handle_paste()
                elif len(self.email) < 20 and len(self.password) < 20:
                    if self.active_input == "email":
                        self.email += event.unicode
                    elif self.active_input == "password":
                        self.password += event.unicode