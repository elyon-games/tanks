import pygame
from client.lib.screen.base import Screen
from client.lib.me import getData
from client.composants import NavBar, showRank
from client.lib.classement import getClassement

class classementScreen(Screen):
    def __init__(self, window):
        super().__init__(window, "classement", "Classement")
        self.user = getData().get("user")
        self.navbar = NavBar(window, self.user)
        self.type = ["kills", "deaths", "kd", "wins", "loses", "wl", "points"]
        self.current_type_index = 0
        self.page = 1
        self.items_per_page = 5
        self.font = pygame.font.Font(None, 36)
        self.updateClassement()

    def updateClassement(self):
        self.classement = getClassement(self.type[self.current_type_index], self.page, self.items_per_page)

    def UpdateView(self):
        self.surface.blit(self.navbar.render(), (0, 0))
        self.renderTypeSelector()
        self.renderClassement()

    def renderTypeSelector(self):
        x_offset = 50
        y_offset = 100  # Adjusted y_offset to move the selector down
        for index, type_name in enumerate(self.type):
            color = (255, 255, 255) if index == self.current_type_index else (100, 100, 100)
            text = self.font.render(type_name, True, color)
            self.surface.blit(text, (x_offset, y_offset))
            x_offset += 100

    def renderClassement(self):
        y_offset = 150  # Adjusted y_offset to move the classement down
        card_height = 60
        card_margin = 10
        for item in self.classement:
            card_rect = pygame.Rect(50, y_offset, 700, card_height)
            pygame.draw.rect(self.surface, (50, 50, 50), card_rect)
            pygame.draw.rect(self.surface, (255, 255, 255), card_rect, 2)
            
            text = self.font.render(f"#{item['position']} | {item['username']} ({item['rank']}) : {item['value']} {self.type[self.current_type_index]}", True, (255, 255, 255))
            self.surface.blit(text, (60, y_offset + 10))
            y_offset += card_height + card_margin

        self.pagination_y_offset = y_offset  # Save the y_offset for pagination buttons
        prev_text = self.font.render("Précédent", True, (255, 255, 255))
        next_text = self.font.render("Suivant", True, (255, 255, 255))
        page_text = self.font.render(f"Page {self.page}", True, (255, 255, 255))
        
        self.surface.blit(prev_text, (50, self.pagination_y_offset + 20))
        self.surface.blit(page_text, (150, self.pagination_y_offset + 20))
        self.surface.blit(next_text, (250, self.pagination_y_offset + 20))

    def HandleEvent(self, type, event):
        self.navbar.HandleEvent(type, event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 50 <= event.pos[0] <= 150 and self.pagination_y_offset + 20 <= event.pos[1] <= self.pagination_y_offset + 70:
                self.page = max(1, self.page - 1)
                self.updateClassement()
            elif 200 <= event.pos[0] <= 300 and self.pagination_y_offset + 20 <= event.pos[1] <= self.pagination_y_offset + 70:
                self.page += 1
                self.updateClassement()
            elif 50 <= event.pos[1] <= 150:
                x_offset = 50
                for index in range(len(self.type)):
                    if x_offset <= event.pos[0] <= x_offset + 100:
                        self.current_type_index = index
                        self.page = 1
                        self.updateClassement()
                        break
                    x_offset += 100
