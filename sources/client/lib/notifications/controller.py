import pygame
import time
from client.types import WINDOW

# Class d'une notification
class Notification:
    def __init__(self, message: str, duration: int=3) -> None:
        self.message = message
        self.duration = duration
        self.start_time = time.time()
    
    # Vérifie si la notification est expirée
    def isExpired(self):
        return time.time() - self.start_time > self.duration

    # Rendu de la notification
    def render(self, window: WINDOW, y_offset: int) -> None:
        window_width = window.get_width()
        window_height = window.get_height()
        
        font_size = int(window_height * 0.05)
        padding = int(window_height * 0.02)
        
        font = pygame.font.Font(None, font_size)
        text = font.render(self.message, True, (255, 255, 255))
        text_rect = text.get_rect(midtop=(window_width // 2, padding + y_offset))        
        background_rect = text_rect.inflate(padding * 2, padding * 2)        
        pygame.draw.rect(window, (0, 0, 0), background_rect, border_radius=10)
        window.blit(text, text_rect.move(padding, padding))

# Global variables
notifications: list[Notification] = []

# Fonction pour afficher une notification
def showNotification(message: str, duration: int= 3) -> None:
    notifications.append(Notification(message, duration))

# Fonction pour mettre à jour les notifications
def updateNotifications(window: WINDOW) -> None:
    window_height = window.get_height()
    y_offset = 0
    for notification in notifications:
        if notification.isExpired():
            notifications.remove(notification)
        else:
            notification.render(window, y_offset)
            y_offset += int(window_height * 0.1)

# Fonction pour récupérer toutes les notifications 
def getAll() -> list[Notification]:
    return notifications