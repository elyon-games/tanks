import pygame
from client.types import EVENTS, KEYS, EVENT, WINDOW
from client.lib.events.controller import getEvents
from client.lib.keys.controler import getKeys
from client.lib.title import changeTitle
class Screen():
    def __init__(self, window: WINDOW, id: str, title: str = None):
        self.id = id
        self.title = title
        self.window: WINDOW = window
        self.keys: KEYS = None
        self.events: EVENTS = None
        self.surface = None
        self.updateSurface(self.getSize())
        self.isMounted = True
    
    def updateSurface(self, size):
        self.surface = pygame.Surface(size, pygame.RESIZABLE)

    def getSize(self):
        if self.window is None:
            return (0, 0)
        return self.window.get_size()

    def UnMount(self):
        self.surface = None
        self.isMounted = False

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

    def calculate_position(self, percentage_x, percentage_y, size_x=0, size_y=0):
        x = int(self.surface.get_width() * (percentage_x / 100) - size_x / 2)
        y = int(self.surface.get_height() * (percentage_y / 100) - size_y / 2)
        return x, y