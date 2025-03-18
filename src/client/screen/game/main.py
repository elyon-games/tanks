import pygame
from client.lib.screen.base import Screen
from client.game.main import Game
from client.types import WINDOW

class gameMainScreen(Screen):
    def __init__(self, window: WINDOW):
        super().__init__(window, "game-main", "Jeu")
        self.game = Game(window.get_width(), window.get_height())

    def UpdateView(self):
        self.game.game()
