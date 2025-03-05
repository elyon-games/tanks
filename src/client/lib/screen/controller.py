import pygame
from typing import  Type
from client.types import EVENTS, WINDOW
from client.lib.screen.base import Screen

actualScreen: Screen = None
actualWindow: WINDOW = None

def getScreenClass(screen_name: str) -> Type[Screen]:
    if screen_name == "loading":
        from client.screen.loading import loadingScreen
        return loadingScreen
    elif screen_name == "home":
        from client.screen.home import HomeScreen
        return HomeScreen
    elif screen_name == "auth-login":
        from client.screen.auth.login import AuthLoginScreen
        return AuthLoginScreen
    elif screen_name == "auth-register":
        from client.screen.auth.register import AuthRegisterScreen
        return AuthRegisterScreen
    elif screen_name == "shop":
        from client.screen.shop import shopScreen
        return shopScreen
    elif screen_name == "profil":
        from client.screen.profil import profilScreen
        return profilScreen
    elif screen_name == "settings":
        from client.screen.settings import settingsScreen
        return settingsScreen
    elif screen_name == "game-main":
        from client.screen.game.main import gameMainScreen
        return gameMainScreen
    elif screen_name == "game-end":
        from client.screen.game.end import gameEndScreen
        return gameEndScreen
    elif screen_name == "game-wait":
        from client.screen.game.wait import gameWaitScreen
        return gameWaitScreen
    elif screen_name == "classement":
        from client.screen.classement import classementScreen
        return classementScreen
    elif screen_name == "parties":
        from client.screen.parties import partiesScreen
        return partiesScreen
    elif screen_name == "create-party":
        from client.screen.create_party import createPartyScreen
        return createPartyScreen
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
        screen_class = getScreenClass(screen)
        actualScreen = screen_class(actualWindow)
    else:
        raise Exception(f"Screen {screen} not found.")
    
    return actualScreen

def getActualScreen() -> Screen:
    global actualScreen
    return actualScreen.id

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
