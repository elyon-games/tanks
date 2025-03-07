import pygame
from client.style.gradient import draw_gradient
from client.style.constants import EMERAUDE, BLEU, WHITE, BLACK, GRAY, STEEL_BLUE, LIGHTER_BLUE, CARD_COLOR, CARD_BORDER_COLOR
from client.style.fonts import getFontSize
from client.lib.screen.base import Screen
from client.types import EVENTS, KEYS
from client.lib.title import changeTitle
from client.lib.auth import register  # Assuming you have a register function
from client.lib.screen.controller import showScreen

class AuthRegisterScreen(Screen):
    def __init__(self, window):
        super().__init__(window, "auth-register", "S'inscrire")
        self.username = ""
        self.email = ""
        self.password = ""
        self.confirm_password = ""
        self.active_input = None
        self.error_message = ""

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

    def render_error_message(self):
        if self.error_message:
            error_surface = getFontSize(24).render(self.error_message, True, (255, 0, 0))
            self.surface.blit(error_surface, ((self.surface.get_width() - error_surface.get_width()) // 2, 350))

    def handle_paste(self):
        try:
            clipboard_text = pygame.scrap.get(pygame.SCRAP_TEXT).decode('utf-8')
            if self.active_input == "username":
                self.username += clipboard_text
            elif self.active_input == "email":
                self.email += clipboard_text
            elif self.active_input == "password":
                self.password += clipboard_text
            elif self.active_input == "confirm_password":
                self.confirm_password += clipboard_text
        except Exception as e:
            print(f"Erreur lors du collage: {e}")

    def render_label(self, text, rect):
        label_surface = getFontSize(24).render(text, True, WHITE)
        self.surface.blit(label_surface, (rect.x, rect.y - 40))

    def UpdateView(self):
        # Background
        draw_gradient(self.surface, EMERAUDE, BLEU, self.surface.get_width(), self.surface.get_height())

        # Center card dimensions
        card_width, card_height = 400, 450
        card_x = (self.surface.get_width() - card_width) // 2
        card_y = (self.surface.get_height() - card_height) // 2

        # Draw card with rounded corners
        self.draw_rounded_rect(self.surface, (card_x, card_y, card_width, card_height), CARD_COLOR, border_radius=20, border_color=CARD_BORDER_COLOR, border_width=2)

        # Input fields
        self.username_rect = pygame.Rect(card_x + 50, card_y + 70, 300, 40)
        self.email_rect = pygame.Rect(card_x + 50, card_y + 130, 300, 40)
        self.password_rect = pygame.Rect(card_x + 50, card_y + 190, 300, 40)
        self.confirm_password_rect = pygame.Rect(card_x + 50, card_y + 250, 300, 40)

        # Render labels
        self.render_label("Nom d'utilisateur", self.username_rect)
        self.render_label("Email", self.email_rect)
        self.render_label("Mot de passe", self.password_rect)
        self.render_label("Confirmer le mot de passe", self.confirm_password_rect)

        self.render_text_input(self.username_rect, self.username, self.active_input == "username")
        self.render_text_input(self.email_rect, self.email, self.active_input == "email")
        self.render_text_input(self.password_rect, "*" * len(self.password), self.active_input == "password")
        self.render_text_input(self.confirm_password_rect, "*" * len(self.confirm_password), self.active_input == "confirm_password")

        # Button
        self.button_rect = pygame.Rect(card_x + 150, card_y + 300, 100, 40)
        mouse_pos = pygame.mouse.get_pos()
        button_hover = self.button_rect.collidepoint(mouse_pos)
        self.render_button(self.button_rect, "S'inscrire", button_hover)

        # Error message
        self.render_error_message()

    def HandleEvent(self, type, event):
        if type == pygame.MOUSEBUTTONDOWN:
            if self.username_rect.collidepoint(event.pos):
                self.active_input = "username"
            elif self.email_rect.collidepoint(event.pos):
                self.active_input = "email"
            elif self.password_rect.collidepoint(event.pos):
                self.active_input = "password"
            elif self.confirm_password_rect.collidepoint(event.pos):
                self.active_input = "confirm_password"
            elif self.button_rect.collidepoint(event.pos):
                self.active_input = None
                if self.password != self.confirm_password:
                    self.error_message = "Les mots de passe ne correspondent pas"
                elif register(self.username, self.email, self.password):
                    showScreen("home")
                    self.error_message = ""
                else:
                    self.password = ""
                    self.confirm_password = ""
                    self.error_message = "Erreur lors de l'inscription"
            else:
                self.active_input = None
        elif type == pygame.KEYDOWN and self.active_input:
            if event.key == pygame.K_BACKSPACE:
                if self.active_input == "username":
                    self.username = self.username[:-1]
                elif self.active_input == "email":
                    self.email = self.email[:-1]
                elif self.active_input == "password":
                    self.password = self.password[:-1]
                elif self.active_input == "confirm_password":
                    self.confirm_password = self.confirm_password[:-1]
            elif event.key == pygame.K_v and (self.keys[pygame.K_LCTRL] or self.keys[pygame.K_RCTRL]):
                self.handle_paste()
            elif len(self.username) < 20 and len(self.email) < 20 and len(self.password) < 20 and len(self.confirm_password) < 20:
                if self.active_input == "username":
                    self.username += event.unicode
                elif self.active_input == "email":
                    self.email += event.unicode
                elif self.active_input == "password":
                    self.password += event.unicode
                elif self.active_input == "confirm_password":
                    self.confirm_password += event.unicode
