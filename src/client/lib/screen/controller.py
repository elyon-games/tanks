import pygame
from typing import Type
from client.types import EVENTS, WINDOW
from client.lib.screen.base import Screen

# Screen Manager System (SMS) Controller

# Global variables
actualScreen: Screen = None
actualWindow: WINDOW = None
historyScreen: list = []

# Arguments
args: dict = {}

# Fonction pour récupérer la classe d'un écran en fonction de son nom
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
    elif screen_name == "create-party":
        from client.screen.create_party import createPartyScreen
        return createPartyScreen
    else:
        raise Exception(f"Screen {screen_name} not found.")
    
# Fonction pour "démonter" l'écran actuel
def UnMountScreen():
    global actualScreen
    if actualScreen is not None and actualScreen.isMounted:
        actualScreen.UnMount()
        actualScreen = None

# Fonction pour revenir à l'écran précédent
def backScreen():
    global actualScreen, actualWindow, historyScreen
    if historyScreen:
        previous_screen = historyScreen.pop()
        showScreen(previous_screen)

# Fonction pour afficher un écran
def showScreen(screen: str) -> Screen:
    global actualScreen, actualWindow, historyScreen
    if actualScreen is not None and actualScreen.id == screen:
        return actualScreen
    elif actualScreen is None or actualScreen.id != screen:
        if actualScreen is not None:
            historyScreen.append(actualScreen.id)
        UnMountScreen()
        screen_class = getScreenClass(screen)
        actualScreen = screen_class(actualWindow)
    else:
        raise Exception(f"Screen {screen} not found.")
    
    return actualScreen

# Fonction pour récupérer l'écran actuel
def getActualScreen() -> Screen:
    global actualScreen
    return actualScreen.id

# Fonction pour mettre à jour l'écran actuel avec les événements
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

# Fonction pour définir un argument pour l'écran actuel
def setArgs(key: str, value: any):
    global args
    args[key] = value

# Fonction pour récupérer un argument de l'écran actuel
def getArgs(key: str) -> any:
    global args
    return args.get(key, None)

# Fonction pour effacer les arguments de l'écran actuel
def clearArgs():
    global args
    args = {}