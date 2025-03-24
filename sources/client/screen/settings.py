import pygame
from client.lib.screen.base import Screen
from client.composants import NavBar
from client.lib.me import getData
from client.lib.settings import get_control, set_control
from client.style.fonts import getFont

class settingsScreen(Screen):
    def __init__(self, window):
        super().__init__(window, "settings", "Paramètres")
        self.user = getData().get("user")
        self.navbar = NavBar(window, self.user)
        self.pressed = {}
        self.modify_key = None
        self.smallfont = getFont("medium")

        self.main_title = getFont("titre").render("Paramètres", True, (255, 255, 255))
        self.key_mappings = {
            "up_key": ("Haut", 210),
            "down_key": ("Bas", 260),
            "left_key": ("Gauche", 310),
            "right_key": ("Droite", 360),
            "shoot_key": ("Tirer", 410)
        }

    def draw_rect(self, y, active):
        color = (75, 75, 75) if active else (50, 50, 50)
        pygame.draw.rect(self.surface, color, [self.surface.get_width() / 2 - 150 / 2, y, 150, 40])

    def UpdateView(self):
        self.surface.blit(self.navbar.render(), (0, 0))
        self.surface.blit(self.main_title, (self.surface.get_width() / 2 - self.main_title.get_width() / 2, 50))

        for key, (label, y) in self.key_mappings.items():
            text = self.smallfont.render(label, True, (255, 255, 255))
            self.surface.blit(text, (self.surface.get_width() / 2 - text.get_width() - 200 / 2, y))
            self.draw_rect(y - 10, self.modify_key == key)
            key_text = self.smallfont.render(get_control(key), True, (255, 255, 255))
            self.surface.blit(key_text, (self.surface.get_width() / 2 - 150 / 2 + 10, y))

    def HandleEvent(self, type, event):
        if not self.surface:
            return
        self.navbar.HandleEvent(type, event)
        if event.type == pygame.KEYDOWN:
            self.pressed[event.key] = True
            if event.key == pygame.K_ESCAPE:
                self.modify_key = None
            elif self.modify_key:
                set_control(self.modify_key, pygame.key.name(event.key))
                self.modify_key = None
        elif event.type == pygame.KEYUP:
            self.pressed[event.key] = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for key, (_, y) in self.key_mappings.items():
                if self.window.get_width() / 2 - 150 / 2 <= event.pos[0] <= self.window.get_width() / 2 + 150 / 2 and y - 10 <= event.pos[1] <= y + 30:
                    self.modify_key = key
                    break
            else:
                self.modify_key = None
