import pygame
from client.types import EVENTS, KEYS, EVENT, WINDOW
from client.lib.events.controller import getEvents
from client.lib.keys.controler import getKeys
from client.lib.title import changeTitle
class Screen():
    # Initialisation de la classe Screen
    # Cette classe est la classe de base pour tous les écrans de l'application
    # Elle gère la création de la surface, le titre de la fenêtre et les événements
    def __init__(self, window: WINDOW, id: str, title: str = None):
        self.id = id
        self.title = title
        self.window: WINDOW = window
        self.keys: KEYS = None
        self.events: EVENTS = None
        self.surface = None
        self.updateSurface(self.getSize())
        self.isMounted = True
    
    # Update la taille de la surface
    def updateSurface(self, size):
        self.surface = pygame.Surface(size, pygame.RESIZABLE)

    # Récupère la taille de la fenêtre
    def getSize(self):
        if self.window is None:
            return (0, 0)
        return self.window.get_size()

    # Récupère la taille de la surface
    def UnMount(self):
        self.surface = None
        self.isMounted = False

    # Met à jour la fenêtre avec la surface
    def Update(self, window):
        if self.isMounted:
            changeTitle(self.title)
            self.window = window
            self.events = getEvents()
            self.keys = getKeys()
            self.window.blit(self.surface, (0, 0), self.surface.get_rect())

    def UpdateView(self):
        pass

    def HandleEvent(self, type: int, event: EVENT):
        pass

    # Fonction pour calculer la position d'un élément sur l'écran en fonction d'un pourcentage (ABANDONNE)
    def calculate_position(self, percentage_x, percentage_y, size_x=0, size_y=0):
        x = int(self.surface.get_width() * (percentage_x / 100) - size_x / 2)
        y = int(self.surface.get_height() * (percentage_y / 100) - size_y / 2)
        return x, y