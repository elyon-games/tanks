import pygame
class ScrollBar:
    def __init__(self, x, y, width, height, content_height, window_height):
        self.rect = pygame.Rect(x, y, width, height)
        self.content_height = content_height
        self.window_height = window_height
        self.scroll_position = 0
        self.scroll_ratio = self.window_height / self.content_height if self.content_height > self.window_height else 1
        self.thumb_height = max(self.scroll_ratio * height, 20)
        self.thumb_rect = pygame.Rect(x, y, width, self.thumb_height)
        self.dragging = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.thumb_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.move_thumb(event.rel[1])
        elif event.type == pygame.MOUSEWHEEL:
            self.move_thumb(-event.y * 20)

    def move_thumb(self, dy):
        self.thumb_rect.y += dy
        self.thumb_rect.y = max(self.rect.top, min(self.thumb_rect.y, self.rect.bottom - self.thumb_rect.height))
        self.scroll_position = (self.thumb_rect.y - self.rect.y) / (self.rect.height - self.thumb_rect.height)

    def get_offset(self):
        return -self.scroll_position * (self.content_height - self.window_height)

    def draw(self, surface):
        pygame.draw.rect(surface, (200, 200, 200), self.rect)
        pygame.draw.rect(surface, (100, 100, 100), self.thumb_rect)
