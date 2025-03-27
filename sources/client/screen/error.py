import pygame
from client.lib.screen.base import Screen
from client.game.main import Game
from client.types import WINDOW
from client.style.gradient import draw_gradient
from client.style.constants import EMERAUDE, RED

class errorScreen(Screen):
    def __init__(self, window: WINDOW, message: str):
        super().__init__(window, "error", "Erreur")
        self.message = message

    def UpdateView(self):
        draw_gradient(self.surface, EMERAUDE, RED, *self.getSize())
        font = pygame.font.Font(None, 36)
        text = font.render(self.message, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.window.get_width() // 2, self.window.get_height() // 2))
        self.surface.blit(text, text_rect)