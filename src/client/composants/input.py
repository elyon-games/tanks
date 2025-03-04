import pygame
from client.style.constants import EMERAUDE, BLEU, WHITE, BLACK, GRAY, STEEL_BLUE, LIGHTER_BLUE, CARD_COLOR, CARD_BORDER_COLOR
from client.style.fonts import getFontSize
from client.lib.keys import getKeys

class Input:
    def __init__(self):
      self.user_input=""
      self.is_active = False

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
    
    def render(self, surface, rect, text=""):
        border_color = WHITE
        self.draw_rounded_rect(surface, rect, BLACK, border_radius=10)
        pygame.draw.rect(surface, border_color, rect, 2, border_radius=10)
        text_surface = getFontSize(32).render(text, True, WHITE)
        surface.blit(text_surface, (rect.x + 10, rect.y + 8))

    def get_input(self):
        try:
            print(getKeys())
            for event in pygame.event.get():
                if event.key == pygame.K_DELETE:
                    del self.user_input[-1]
                try:
                    print(f"key{pygame.key.name(event.key)}")
                    self.user_input += pygame.key.name(event.key) or ""
                except:
                    pass

                return self.user_input
            
        except Exception as e:
            print(e)

