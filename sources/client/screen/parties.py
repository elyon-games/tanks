import pygame
from client.lib.screen.base import Screen
from client.lib.me import getData
from client.composants import NavBar
from client.lib.utils import getMaps

class partiesScreen(Screen):
    def __init__(self, window):
        super().__init__(window, "parties", "Parties")
        self.user = getData().get("user")
        self.navbar = NavBar(window, self.user)
        self.maps: list[dict] = getMaps()
        self.show_modal = False
        self.is_private = False
        self.selected_map = None
        self.create_button = pygame.Rect(50, 50, 200, 50)
        self.map_buttons = []
        self.dropdown_open = False

    def UpdateView(self):
        self.surface.blit(self.navbar.render(), (0, 0))
        pygame.draw.rect(self.surface, (0, 128, 255), self.create_button)
        font = pygame.font.Font(None, 36)
        text = font.render('Créer une partie', True, (255, 255, 255))
        self.surface.blit(text, (self.create_button.x + 10, self.create_button.y + 10))

        if self.show_modal:
            self.draw_modal()

    def draw_modal(self):
        modal_rect = pygame.Rect(100, 100, 400, 300)
        pygame.draw.rect(self.surface, (200, 200, 200), modal_rect)
        font = pygame.font.Font(None, 36)
        text = font.render('Créer une partie', True, (0, 0, 0))
        self.surface.blit(text, (modal_rect.x + 10, modal_rect.y + 10))

        private_checkbox = pygame.Rect(modal_rect.x + 10, modal_rect.y + 50, 20, 20)
        pygame.draw.rect(self.surface, (0, 0, 0), private_checkbox, 2)
        if self.is_private:
            pygame.draw.rect(self.surface, (0, 0, 0), private_checkbox)

        text = font.render('Partie privée', True, (0, 0, 0))
        self.surface.blit(text, (private_checkbox.x + 30, private_checkbox.y))

        map_selector = pygame.Rect(modal_rect.x + 10, modal_rect.y + 100, 380, 30)
        pygame.draw.rect(self.surface, (0, 0, 0), map_selector, 2)
        if self.selected_map:
            text = font.render(self.selected_map["name"], True, (0, 0, 0))
            self.surface.blit(text, (map_selector.x + 10, map_selector.y + 5))
        else:
            text = font.render('Select a map', True, (0, 0, 0))
            self.surface.blit(text, (map_selector.x + 10, map_selector.y + 5))

        if self.dropdown_open:
            self.map_buttons = []
            for i, map_data in enumerate(self.maps):
                map_button = pygame.Rect(modal_rect.x + 10, modal_rect.y + 140 + i * 40, 380, 30)
                pygame.draw.rect(self.surface, (0, 0, 0), map_button, 2)
                text = font.render(map_data["name"], True, (0, 0, 0))
                self.surface.blit(text, (map_button.x + 10, map_button.y + 5))
                self.map_buttons.append((map_button, map_data))

    def HandleEvent(self, type, event):
        self.navbar.HandleEvent(type, event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.create_button.collidepoint(event.pos):
                self.show_modal = True
            elif self.show_modal:
                modal_rect = pygame.Rect(100, 100, 400, 300)
                private_checkbox = pygame.Rect(modal_rect.x + 10, modal_rect.y + 50, 20, 20)
                if private_checkbox.collidepoint(event.pos):
                    self.is_private = not self.is_private

                map_selector = pygame.Rect(modal_rect.x + 10, modal_rect.y + 100, 380, 30)
                if map_selector.collidepoint(event.pos):
                    self.dropdown_open = not self.dropdown_open
                elif self.dropdown_open:
                    for map_button, map_data in self.map_buttons:
                        if map_button.collidepoint(event.pos):
                            self.selected_map = map_data
                            self.dropdown_open = False
                            break
                else:
                    self.dropdown_open = False