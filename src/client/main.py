import time
import traceback
import json
import os
import sys
import pygame

import common.process as process
from common.config import getConfig, setConfigParameter
from common.random import generate_random_uuid
from common.args import getArgs

pygame.init()
pygame.font.init()
pygame.mixer.init()

import common.path as path
import common.errors as errors
from client.lib.title import changeTitle
from client.lib.ping import ping
from client.style.constants import WHITE
from client.style.fonts import getFont
from client.lib.screen.controller import showScreen, updateScreen
from client.lib.keys.controler import updateKeys
from client.lib.notifications.controller import updateNotifications
from client.lib.events.controller import updateEvents
from client.lib.storage.controller import createStorage
from client.lib.assets import loadAsset
from client.lib.auth import verify as auth_verify
from client.var import auth as authData
import hashlib

import tkinter as tk
from tkinter import messagebox

def stopAllProcesses():
    config = getConfig("client")
    pygame.quit()
    if config["launch"]["type"] == "local":
        for proces in process.get_all_processes().values():
            proces.stop()

def Main():
    try:
        config = getConfig("client")
        options = getArgs()
        global window, clock, ms_per_frame, authData
        ms_per_frame = 10
        pygame.display.set_icon(loadAsset("app-icon", "/logo/round.ico"))
        changeTitle("Chargment...")
        window_width, window_height = 800, 600
        window = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
        clock = pygame.time.Clock()
        client_data_path = path.get_path("client_data")
        client_data_servers_path = path.get_path("client_data_servers")

        commonStorage = createStorage("common", client_data_path, {"time": time.time()})
        computer_id: str = ""
        if "computer_id" not in commonStorage.getData():
            computer_id = generate_random_uuid()
            commonStorage.addData("computer_id", computer_id)
            commonStorage.saveData()
        else:
            computer_id = commonStorage.getData()["computer_id"]
        setConfigParameter("client", "computer_id", computer_id)
        config = getConfig("client")

        changeTitle("Chargement...")

        pingData = ping()
        if pingData.get("version") != config["version"]:
            raise ValueError(errors.getErrorMessage("CLIENT_VERSION_MISMATCH"))
        
        if pingData.get("key") is None:
            raise ValueError(errors.getErrorMessage("SERVER_MISSING_KEY"))

        serverKey = pingData.get("key")
        serverLocalID = hashlib.md5(f"{serverKey}{config['server']['host']}".encode('utf-8')).hexdigest()

        setConfigParameter("server", "server.id", serverLocalID)

        serverStorage = createStorage(serverLocalID, client_data_servers_path, {"time": time.time()})

        process.started_callback("client-main")

        def initLoading():
            print("Init Screen")
            showScreen("loading")
            time.sleep(0.5)
            loadAsset("logo", "/logo/round.png")
            token = serverStorage.getKey("token")
            if token:
                verifyData = auth_verify(token)
                if verifyData.get("status"):
                    authData["user_id"] = verifyData["user_id"]
                    authData["token"] = token
                    showScreen("home")
                else:
                    showScreen("auth-login")
            else:
                showScreen("auth-login")

        running = True
        init = False
        debugView = False
        authStatus = False
        while running:
            events = pygame.event.get()
            keys = pygame.key.get_pressed()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F3:
                        debugView = not debugView 
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.VIDEORESIZE:
                    window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            window.fill((0, 0, 0))

            updateKeys(keys)
            updateEvents(events)
            updateScreen(window, events)
            updateNotifications(window)
            if not init:
                init = True
                process.create_process("client-init-loading", initLoading).start()

            if not authStatus and authData.get("token", None):
                verifyData = auth_verify(authData["token"])
                if verifyData.get("status", None):
                    authData["user_id"] = verifyData["user_id"]
                    serverStorage.addData("token", authData["token"])
                    serverStorage.saveData()
                    showScreen("home")
                    authStatus = True
                else:
                    authData = False
                    showScreen("auth-login")
                
            fps = int(clock.get_fps())
            current_ms_per_frame = clock.get_time()
            if abs(current_ms_per_frame - ms_per_frame) >= 5:
                ms_per_frame = current_ms_per_frame

            if debugView:
                computer_id_text = getFont("hud_info").render(f"CLIENT : {'-'.join(computer_id.split('-')[:2])}", True, WHITE)
                fps_text = getFont("hud_info").render(f"FPS : {fps}", True, WHITE)
                ms_text = getFont("hud_info").render(f"MSPF : {ms_per_frame}", True, WHITE)
                pygame_version = getFont("hud_info").render(f"Pygame : {pygame.version.ver}", True, WHITE)
    
                window.blit(computer_id_text, (10, 10))
                window.blit(fps_text, (10, 25))
                window.blit(ms_text, (10, 40))
                window.blit(pygame_version, (10, 55))
                
            pygame.display.flip()
            clock.tick(100)

        stopAllProcesses()

    except Exception as exc:
        #ajouter un except pour si il n'arrive pas a se connecter au serveur

        def show_error_message(message, detail):
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Erreur", message, detail=detail)
            root.destroy()

        error_message = f"Une erreur s'est produite : {exc}"
        error_detail = traceback.format_exc()
        print(error_message, error_detail)
        show_error_message(error_message, error_detail)
        stopAllProcesses()