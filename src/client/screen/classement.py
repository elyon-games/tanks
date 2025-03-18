import pygame
from client.lib.screen.base import Screen
from client.lib.me import getData
from client.composants import NavBar, showRank, showUsername
from client.lib.classement import getClassement
from client.style.fonts import getFontSize
from client.lib.utils import getUserIDWithUsername
from client.lib.nav import goProfil

class classementScreen(Screen):
    def __init__(self, window):
        super().__init__(window, "classement", "Classement")
        self.user = getData().get("user")
        self.navbar = NavBar(window, self.user)
        self.type = ["points", "wins", "kd", "kills", "deaths", "loses", "wl"]
        self.current_type_index = 0
        self.page = 1
        self.items_per_page = 5
        self.font = pygame.font.Font(None, 36)
        self.buttons_type_rects = []
        self.username_rects = []
        self.updateClassement()

    def updateClassement(self):
        self.classement = getClassement(self.type[self.current_type_index], self.page, self.items_per_page)

    def UpdateView(self):
        self.surface.blit(self.navbar.render(), (0, 0))
        self.renderTypeSelector()
        self.renderClassement()

    def renderTypeSelector(self):
        x_offset = self.window.get_width()*0.1
        y_offset = 140  # Adjusted y_offset to move the selector down
        for index, type_name in enumerate(self.type):
            color = (255, 255, 255) if index == self.current_type_index else (100, 100, 100)
            x_offset += (self.window.get_width() - self.window.get_width()*0.1 - 180)/len(self.type)
            self.buttons_type_rects.append(pygame.Rect(x_offset-100, y_offset, 80*(x_offset*1.1/x_offset), 30))
            self.render_label(type_name, self.buttons_type_rects[index])

    def renderClassement(self):
        y_offset = 190  # Adjusted y_offset to move the classement down
        card_height = 60
        card_margin = 10
        self.username_rects = []
        for item in self.classement:
            card_rect = pygame.Rect(50, y_offset, self.window.get_width()*0.9, card_height)
            pygame.draw.rect(self.surface, (50, 50, 50), card_rect)
            pygame.draw.rect(self.surface, (255, 255, 255), card_rect, 2)
            
            position_text = self.font.render(f"#{item['position']} ", True, (255, 255, 255))
            self.surface.blit(position_text, (card_rect.width*1.1 - card_rect.width, y_offset + 10))
            
            username = showUsername(self.window, item['username'], item['rank'])
            username_rect = username.render().get_rect(topleft=(card_rect.width*1.2 - card_rect.width, y_offset + 10))
            self.username_rects.append((username_rect, item['username']))
            self.surface.blit(username.render(), username_rect)            
            
            value_text = self.font.render(f" {item['value']}", True, (255, 255, 255))
            self.surface.blit(value_text, (card_rect.width*1.5-card_rect.width, y_offset + 10))
            
            y_offset += card_height + card_margin

        self.pagination_y_offset = y_offset

        self.precedent_button = pygame.Rect(self.window.get_width()/2 - 200, self.pagination_y_offset + 10, 100, 30)
        self.page_button = pygame.Rect(self.window.get_width()/2 - 50,self.pagination_y_offset + 10, 100, 30)
        self.suivant_button = pygame.Rect(self.window.get_width()/2 + 100, self.pagination_y_offset + 10, 100, 30)
        self.render_label("Précédent", self.precedent_button)
        self.render_label(f"Page {self.page}", self.page_button)
        self.render_label("Suivant", self.suivant_button)

    def render_label(self, text, rect): 
        label_surface = getFontSize(30).render(text, True, (255, 255, 255))
        self.surface.blit(label_surface, (rect.x, rect.y))

    def HandleEvent(self, type, event):
        self.navbar.HandleEvent(type, event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if self.precedent_button.collidepoint(mouse_pos):
                self.page = max(1, self.page - 1)
                self.updateClassement()
            elif self.suivant_button.collidepoint(mouse_pos):
                self.page += 1
                self.updateClassement()
            for button_rect in self.buttons_type_rects:
                if button_rect.collidepoint(mouse_pos):
                    self.current_type_index = self.buttons_type_rects.index(button_rect)
                    self.page = 1
                    self.updateClassement()
                    break
            for username_rect, username in self.username_rects:
                if username_rect.collidepoint(mouse_pos):
                    user_id = getUserIDWithUsername(username)
                    goProfil(user_id)
                    break
