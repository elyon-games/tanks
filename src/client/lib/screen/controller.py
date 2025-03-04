import pygame
from typing import  Type
from client.types import EVENTS, WINDOW
from client.lib.screen.base import Screen

actualScreen: Screen = None
actualWindow: WINDOW = None

def get_screen_class(screen_name: str) -> Type[Screen]:
    if screen_name == "loading":
        from client.screen.loading import loadingScreen
        return loadingScreen
    elif screen_name == "home":
        from client.screen.home import HomeScreen
        return HomeScreen
    elif screen_name == "auth-login":
        from client.screen.auth.login import AuthLoginScreen
        return AuthLoginScreen
    else:
        raise Exception(f"Screen {screen_name} not found.")

def UnMountScreen():
    global actualScreen
    if actualScreen is not None and actualScreen.isMounted:
        actualScreen.UnMount()
        actualScreen = None

def showScreen(screen: str) -> Screen:
    global actualScreen, actualWindow
    if actualScreen is not None and actualScreen.id == screen:
        return actualScreen
    elif actualScreen is None or actualScreen.id != screen:
        UnMountScreen()
        screen_class = get_screen_class(screen)
        actualScreen = screen_class(actualWindow)
    else:
        raise Exception(f"Screen {screen} not found.")
    
    return actualScreen

def updateScreen(window: WINDOW, events: EVENTS):
    global actualScreen, actualWindow
    actualWindow = window
    if actualScreen is not None and actualScreen.isMounted:
        for event in events:
            if event.type == pygame.VIDEORESIZE:
                actualScreen.updateSurface((event.w, event.h))
            actualScreen.HandleEvent(type=event.type, event=event)
        actualScreen.Update(window)
        actualScreen.UpdateView()
