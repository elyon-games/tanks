import pygame
import time
from client.types import WINDOW

class Notification:
    def __init__(self, message, duration):
        self.message = message
        self.duration = duration
        self.start_time = time.time()
    
    def isExpired(self):
        return time.time() - self.start_time > self.duration

    def render(self, window: WINDOW, y_offset):
        window_width = window.get_width()
        window_height = window.get_height()
        
        # Adjust font size and padding based on window size
        font_size = int(window_height * 0.05)
        padding = int(window_height * 0.02)
        
        font = pygame.font.Font(None, font_size)
        text = font.render(self.message, True, (255, 255, 255))
        text_rect = text.get_rect(midtop=(window_width // 2, padding + y_offset))
        
        # Add padding
        background_rect = text_rect.inflate(padding * 2, padding * 2)
        
        # Draw rounded rectangle
        pygame.draw.rect(window, (0, 0, 0), background_rect, border_radius=10)
        
        # Blit the text onto the window
        window.blit(text, text_rect.move(padding, padding))

notifications: list[Notification] = []

def showNotification(message, duration=3):
    notifications.append(Notification(message, duration))

def updateNotifications(window: WINDOW):
    window_height = window.get_height()
    y_offset = 0
    for notification in notifications:
        if notification.isExpired():
            notifications.remove(notification)
        else:
            notification.render(window, y_offset)
            y_offset += int(window_height * 0.1)  # Adjust vertical spacing based on window height

def getAll():
    return notifications