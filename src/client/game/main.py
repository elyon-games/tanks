import pygame  # Importation de la bibliothèque Pygame pour la création de jeux
import socket  # Importation de la bibliothèque Socket pour les communications réseau
import time  # Importation de la bibliothèque time pour manipuler le temps
import requests  # Importation de la bibliothèque requests pour effectuer des requêtes HTTP
import random  # Importation de la bibliothèque random pour générer des nombres aléatoires
import sys # Importation de la bibliothèque sys pour interagir avec le système
from client.game.tank import Tank  # Importation de la classe Tank depuis le fichier modules/tank.py
from client.game.topTank import TopTank  # Importation de la classe TopTank depuis le fichier modules/topTank.py
from client.game.network import connect_to_server, send_message, receive_messages, close_connection, get_map  # Importation de certaines fonctions depuis le fichier modules/network.py
from client.game.bullet import Bullet  # Importation de la classe Bullet depuis le fichier modules/bullet.py
from client.game.map import getWalls
from client.style.fonts import getFontSize

class Game:  # Définition de la classe Game
    def __init__(self, width=1920, height=1080, background_path=None):  # Définition du constructeur de la classe Game et de ses paramètres
        self.width = width  # Largeur de la fenêtre du jeu
        self.height = height  # Hauteur de la fenêtre du jeu
        self.background_path = pygame.image.load(background_path)  # Chargement de l'image de fond
        self.background = pygame.transform.scale(self.background_path, (self.width, self.height))  # Redimensionnement de l'image de fond
        self.write_port_mode = ""  # Port du serveur (initialisation à vide)
        self.time = 0  # Initialisation du temps
        
        self.pressed = {}  # Dictionnaire pour gérer les touches pressées
        
        self.debug = False  # Mode de débogage
                
        self.freeze = False  # Mode de pause du jeu

        self.status = "menu"  # Statut du jeu (menu, play, options, ingame)
        
        self.connected = False  # Initialisation de la variable indiquant l'état de connexion au serveur
        self.client_socket = None  # Initialisation du socket client
        
        self.is_running = True  # Le jeu est en cours d'exécution
        self.in_main_menu = True  # Le jeu est dans le menu principal
        
        self.in_game = False  # Le jeu n'est pas en cours
        
        self.tanks = []  # Initialisation de la liste des tanks

        self.port = 5556 # Port par défaut
        self.ip = ""

        self.controls = {"up_key" : "z", "down_key": "s", "left_key" : "q", "right_key" : "d", "shoot_key" : "space"} # Initialisation du dictionnaire des contrôles
        
        self.walls = []
        self.map = None

        self.pause = False

        self.waiting = False
        
        self.win = None
        
        self.affichFin = False

        self.firstMessage = True
        
    def setFonts(self):
        # Initialisation des polices de caractères (textes généraux)
        self.smallfont = getFontSize(35)
        self.largefont = getFontSize(75)
        self.mediumfont = getFontSize(50)
        
        # Initialisation des polices de caractères (texte d'attente)
        self.wainting_text = self.mediumfont.render("En attente d'adversaire..." , True , (255,255,255))
        self.waiting_text = self.mediumfont.render("Votre adversaire est en pause..." , True , (255,255,255))

        # Initialisation des polices de caractères (texte menu pause)
        self.pause_text = self.largefont.render("Pause" , True , (255,255,255))
        self.reprendre_text = self.smallfont.render("Reprendre" , True , (255,255,255))
        self.quitter_text = self.smallfont.render("Quitter" , True , (255,255,255))
        
        # Initialisation des polices de caractères (texte d'erreurs)
        self.error1_surface = self.smallfont.render("Le serveur est indisponible !" , True , (255,64,64))  # Création d'une surface de texte
        self.error2_surface = self.smallfont.render("Le serveur est plein !", True, (255, 64, 64))  # Création d'une surface de texte
        self.error3_surface = self.smallfont.render("Le serveur n'éxiste pas !" , True , (255,64,64))  # Création d'une surface de texte
        self.error4_surface = self.smallfont.render("Une erreur est survenue." , True , (255,64,64))  # Création d'une surface de texte
        
        # Initialisation des polices de caractères (texte de fin de partie)
        self.win_text = self.largefont.render("Victoire !" , True , (255,255,255))  # Création d'une surface de texte
        self.loose_text = self.largefont.render("Défaite !" , True , (255,255,255))  # Création d'une surface de texte
    
    def finish(self):
        if self.connected:
            close_connection(self.port, self.ip)  # Fermeture de la connexion
        self.connected = False  # Mise à jour de l'état de connexion
        self.in_main_menu = True  # Retour au menu principal
        for tank in self.tanks:
            tank[0].all_projectiles.empty()
            tank[1].kill()
            tank[0].kill()
        self.tanks = []  # Réinitialisation de la liste des tanks
        self.in_game = False  # Le jeu n'est plus en cours
        self.walls = []
        self.map = None
        self.pause = False
        self.win = None
        self.affichFin = False
        self.waiting = False
        self.firstMessage = True

    def game(self):  # Méthode pour démarrer le jeu
        
        self.setFonts()  # Initialisation des polices de caractères

        message = None  # Initialisation de la variable message (évite les erreurs de type NoneType)
        
        # Boucle principale du jeu
        while self.is_running:
            
            self.screen.blit(self.background, (0,0))  # Affichage de l'image de fond

            for wall in self.walls:
                self.screen.blit(wall.image, wall.rect)
            
            if self.in_game and self.connected:
                # Envoi des données au serveur
                # Préparation des données à envoyer au serveur
                if len(self.tanks) > 1 :
                    data = [[self.tanks[0][0].rect.x, self.tanks[0][0].rect.y], self.tanks[0][0].rotation, self.tanks[0][1].get_angle(), [{"position": [projectile.rect.x, projectile.rect.y], "angle": projectile.angle, "id": projectile.id} for projectile in self.tanks[0][0].all_projectiles], self.tanks[0][0].life, self.pause]
                if self.firstMessage:
                    data = [[self.tanks[0][0].rect.x, self.tanks[0][0].rect.y], self.tanks[0][0].rotation, self.tanks[0][1].get_angle(), [{"position": [projectile.rect.x, projectile.rect.y], "angle": projectile.angle, "id": projectile.id} for projectile in self.tanks[0][0].all_projectiles], 100, 100, self.pause]
                    self.firstMessage = False
                if data != None:
                    send_message(data, self.port, self.ip)
                message = receive_messages(self.port, self.ip)
                
                # Gestion des messages reçus du serveur
                if message == "Finish":
                    print("[CLIENT] Déconnexion du serveur.")
                    self.finish()
            
            if self.in_game and len(self.tanks) == 1:
                
                if not self.affichFin:
                    self.screen.blit(self.wainting_text, (self.width/2 - self.wainting_text.get_width()/2, 70))  # Affichage du titre
                
                self.screen.blit(self.tanks[0][0].image, self.tanks[0][0].rect)  # Affichage du Tank
                self.screen.blit(self.tanks[0][1].image, self.tanks[0][1].rect)  # Affichage du TopTank
                
                if message and type(message) != str and message[0] == "ready":
                    print("[CLIENT] Un adversaire s'est connecté.")
                    self.tanks.append(self.createEnemyTank())
                    wallType = random.choice(["assets/walls/wall1.png", "assets/walls/wall2.png", "assets/walls/wall3.png", "assets/walls/wall4.png"])
                    self.map = get_map()
                    self.walls = getWalls(self, self.map, wallType)
            
            if self.in_game and len(self.tanks) > 1:

                if self.map == None:
                    self.map = get_map()
                    if self.map != None:
                        wallType = random.choice(["assets/walls/wall1.png", "assets/walls/wall2.png", "assets/walls/wall3.png", "assets/walls/wall4.png"])
                        self.walls = getWalls(self, self.map, wallType)
                
                for tank in self.tanks:
                    self.screen.blit(tank[0].image, tank[0].rect)
                    self.screen.blit(tank[1].image, tank[1].rect)
                    tank[0].life_bar()
                
                for tank in self.tanks:
                    for bullet in tank[0].all_projectiles:
                        bullet.update()
                    tank[0].all_projectiles.draw(self.screen)
                
                pygame.display.update()  # Mise à jour de l'affichage
            
            if self.in_main_menu:
                self.mainmenuScreen()  # Affichage de l'écran du menu principal
                self.in_main_menu = False  # Changement du statut du menu
                
            if self.win != None:
                self.AffichageFin()

            if not self.affichFin and self.waiting:
                self.screen.blit(self.waiting_text, (self.width/2 - self.wainting_text.get_width()/2, 70))
            
            pygame.display.update()  # Mise à jour de l'affichage
            
            # Vérification si la fenêtre est fermée
            if not pygame.display.get_init():
                close_connection(self.client_socket)  # Fermeture de la connexion
                self.connected = False  # Mise à jour de l'état de connexion
                self.in_main_menu = True  # Retour au menu principal
                self.tanks = []  # Réinitialisation de la liste des tanks
                self.in_game = False  # Le jeu n'est plus en cours
                break
            
            if self.in_game and len(self.tanks) > 1:
                
                if self.tanks[0][0].life <= 0 or self.win == False:
                    self.win = False
                    self.screen

                if self.pause:
                    self.pauseMenu()  # Affichage du menu de pause
                    self.pause = False  # Désactivation du mode pause
                
                if not self.pause and not self.waiting:
                    # Gestion des entrées utilisateur
                    if self.win == None:
                        self.tanks[0][0].handle_input(self.controls["up_key"], self.controls["down_key"], self.controls["left_key"], self.controls["right_key"], self.controls["shoot_key"])
                    self.tanks[0][1].rotate()  # Rotation du TopTank

                if message and type(message) == list and message[0] != "None":
                    # Mise à jour des informations des tanks ennemis
                    if self.tanks[1][0].rect.x != message[0][0] or self.tanks[1][0].rect.y != message[0][1]:
                        self.tanks[1][0].set_position(message[0])
                        self.tanks[1][0].spriteRotate(message[1])
                        self.tanks[1][0].rotation = message[1]
                    self.tanks[1][1].rotate_with_angle(message[2])
                    for projectile in message[3]:  # Création des nouveaux projectiles
                        if projectile["id"] not in [bullet.id for bullet in self.tanks[1][0].all_projectiles]:
                            self.tanks[1][0].all_projectiles.add(Bullet(self, projectile["id"], angle=projectile["angle"], start=projectile["position"]))
                    for bullet in self.tanks[1][0].all_projectiles:
                        if bullet.id not in [projectile["id"] for projectile in message[3]]:
                            bullet.kill()
                    # On modifie les positions des projectiles existants si elles ne correspondent pas
                    for bullet in self.tanks[1][0].all_projectiles:
                        for projectile in message[3]:
                            if bullet.id == projectile["id"]:
                                if bullet.rect.x != projectile["position"][0] or bullet.rect.y != projectile["position"][1] or bullet.angle != projectile["angle"]:
                                    bullet.rect.x = projectile["position"][0]
                                    bullet.rect.y = projectile["position"][1]
                                    bullet.angle = projectile["angle"]
                                    bullet.newAngle(bullet.angle)
                                    bullet.spriteRotate(bullet.image_custom)
                    self.tanks[1][0].life = self.tanks[1][0].life  # Mise à jour des points de vie du tank ennemi
                    self.waiting = message[5]

                    if self.debug:
                        print(f"[CLIENT] Message reçu: {message}")  # Affichage du message reçu du serveur
                        
                if self.tanks[0][0].life <= 0 or self.tanks[1][0].life <= 0:
                    if self.tanks[0][0].life <= 0:
                        self.win = False
                        for tank in self.tanks:
                            for bullet in tank[0].all_projectiles:
                                bullet.kill()
                        # On retire le tank qui a perdu
                        tank = self.tanks.pop(0)
                        tank[0].kill()
                        tank[1].kill()
                        pygame.display.update()  # Mise à jour de l'affichage
                        
                    else:
                        self.win = True
                        for tank in self.tanks:
                            for bullet in tank[0].all_projectiles:
                                bullet.kill()
                        # On retire le tank qui a perdu
                        tank = self.tanks.pop(1)
                        tank[0].kill()
                        tank[1].kill()
                        pygame.display.update()  # Mise à jour de l'affichage
                    self.affichFin = True

            
            # Gestion des événements
            for event in pygame.event.get():
                # Si l'utilisateur ferme la fenêtre avec la croix ou fait ALT+F4
                if event.type == pygame.QUIT:
                    self.stopGame()  # Arrêt du jeu
                elif event.type == pygame.KEYDOWN:  # Si une touche est pressée
                    self.pressed[event.key] = True  # Enregistrement de la touche pressée
                elif event.type == pygame.KEYUP:  # Si une touche est relâchée
                    self.pressed[event.key] = False  # Enregistrement de la touche relâchée
            
            if(self.pressed.get(pygame.K_ESCAPE)):
                if len(self.tanks) < 2:
                    self.in_main_menu = True
                else:
                    self.pause = not self.pause
                    
    def AffichageFin(self):
        while self.win != None:
            if self.win:
                self.screen.blit(self.win_text, (self.width/2 - self.win_text.get_width()/2, 70))
            else:
                self.screen.blit(self.loose_text, (self.width/2 - self.loose_text.get_width()/2, 70))
            pygame.draw.rect(self.screen,(50,50,50),[self.width/2 - 150/2,490,150,40])
            self.screen.blit(self.main_back, (self.width/2 - self.main_back.get_width()/2, 500))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.width/2 - 150/2 <= event.pos[0] <= self.width/2 + 150/2 and 490 <= event.pos[1] <= 530:
                            self.finish()
                            self.in_main_menu = True
                            self.win = None
                            self.AffichFin = False
                            return None
                elif event.type == pygame.QUIT:
                    self.stopGame()  # Arrêt du jeu
    
    def mainmenuScreen(self):
        self.finish()  # Arrêt de la partie en cours
        is_open = True
        while is_open:
            self.screen.fill((0, 0, 0))  # Remplissage de l'écran en noir

            self.screen.blit(self.main_title, (self.width/2 - self.main_title.get_width()/2, 50))  # Affichage du titre
            pygame.draw.rect(self.screen,(50,50,50),[self.width/2 - 150/2,290,150,40]) 
            self.screen.blit(self.main_play, (self.width/2 - self.main_play.get_width()/2, 300))  # Affichage du bouton "Jouer"
            pygame.draw.rect(self.screen,(50,50,50),[self.width/2 - 150/2,340,150,40])
            self.screen.blit(self.main_options, (self.width/2 - self.main_options.get_width()/2, 350))  # Affichage du bouton "Options"
            pygame.draw.rect(self.screen,(50,50,50),[self.width/2 - 150/2,390,150,40])
            self.screen.blit(self.main_quit, (self.width/2 - self.main_quit.get_width()/2, 400))  # Affichage du bouton "Quitter"

            pygame.display.update()  # Mise à jour de l'affichage

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Si l'utilisateur ferme la fenêtre
                    return self.stopGame()  # Arrêt de Pygame
                elif event.type == pygame.KEYDOWN:  # Si une touche est pressée
                    self.pressed[event.key] = True  # Enregistrement de la touche pressée
                elif event.type == pygame.KEYUP:  # Si une touche est relâchée
                    self.pressed[event.key] = False  # Enregistrement de la touche relâchée
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # Vérification des clics sur les boutons du menu principal
                        if self.width/2 - 150/2 <= event.pos[0] <= self.width/2 + 150/2 and 290 <= event.pos[1] <= 330:
                            self.status = "play"  # Changement de statut pour jouer
                            self.playScreen()  # Affichage de l'écran de jeu
                            if self.status == "ingame":
                                is_open = False
                        elif self.width/2 - 150/2 <= event.pos[0] <= self.width/2 + 150/2 and 390 <= event.pos[1] <= 430:
                            return self.stopGame()  # Arrêt de Pygame
                        elif self.width/2 - 150/2 <= event.pos[0] <= self.width/2 + 150/2 and 340 <= event.pos[1] <= 380:
                            self.status = "options"  # Changement de statut pour les options
                            self.is_running = True
                            self.optionsScreen()  # Affichage de l'écran des options

    def optionsScreen(self):
        is_open = True
        modify_up_key = False  # Variable pour indiquer si le mode de modification est activé
        modify_down_key = False
        modify_left_key = False
        modify_right_key = False
        modify_shoot_key = False

        while is_open:
            self.screen.fill((0, 0, 0))  # Remplissage de l'écran en noir

            self.screen.blit(self.main_title, (self.width/2 - self.main_title.get_width()/2, 50))  # Affichage du titre

            self.screen.blit(self.up_key, (self.width/2 - self.up_key.get_width() - 200/2, 210))  # Affichage du texte "Haut"

            self.screen.blit(self.down_key, (self.width/2 - self.down_key.get_width() - 200/2, 260))  # Affichage du texte "Bas"

            self.screen.blit(self.left_key, (self.width/2 - self.left_key.get_width() - 200/2, 310))  # Affichage du texte "Gauche"

            self.screen.blit(self.right_key, (self.width/2 - self.right_key.get_width() - 200/2, 360))  # Affichage du texte "Droite"

            self.screen.blit(self.shoot_key, (self.width/2 - self.shoot_key.get_width() - 200/2, 410))  # Affichage du texte "Tirer"

            pygame.draw.rect(self.screen,(50,50,50),[self.width/2 - 150/2,490,150,40])
            self.screen.blit(self.main_back, (self.width/2 - self.main_back.get_width()/2, 500)) # Affichage du bouton "Retour"

            if(modify_up_key):
                pygame.draw.rect(self.screen,(75,75,75),[self.width/2 - 150/2,200,150,40])
            else:
                pygame.draw.rect(self.screen,(50,50,50),[self.width/2 - 150/2,200,150,40])
            
            if(modify_down_key):
                pygame.draw.rect(self.screen,(75,75,75),[self.width/2 - 150/2,250,150,40])
            else:
                pygame.draw.rect(self.screen,(50,50,50),[self.width/2 - 150/2,250,150,40])

            if(modify_left_key):
                pygame.draw.rect(self.screen,(75,75,75),[self.width/2 - 150/2,300,150,40])
            else:
                pygame.draw.rect(self.screen,(50,50,50),[self.width/2 - 150/2,300,150,40])

            if(modify_right_key):
                pygame.draw.rect(self.screen,(75,75,75),[self.width/2 - 150/2,350,150,40])
            else:
                pygame.draw.rect(self.screen,(50,50,50),[self.width/2 - 150/2,350,150,40])

            if(modify_shoot_key):
                pygame.draw.rect(self.screen,(75,75,75),[self.width/2 - 150/2,400,150,40])
            else:
                pygame.draw.rect(self.screen,(50,50,50),[self.width/2 - 150/2,400,150,40])

            self.screen.blit(self.smallfont.render(self.controls["up_key"], True, (255,255,255)), (self.width/2 - 150/2 + 10, 210))  # Affichage de la touche associée à "Haut"
            self.screen.blit(self.smallfont.render(self.controls["down_key"], True, (255,255,255)), (self.width/2 - 150/2 + 10, 260))  # Affichage de la touche associée à "Bas"
            self.screen.blit(self.smallfont.render(self.controls["left_key"], True, (255,255,255)), (self.width/2 - 150/2 + 10, 310))  # Affichage de la touche associée à "Gauche"
            self.screen.blit(self.smallfont.render(self.controls["right_key"], True, (255,255,255)), (self.width/2 - 150/2 + 10, 360))  # Affichage de la touche associée à "Droite"
            self.screen.blit(self.smallfont.render(self.controls["shoot_key"], True, (255,255,255)), (self.width/2 - 150/2 + 10, 410))  # Affichage de la touche associée à "Tirer"

            pygame.display.update()  # Mise à jour de l'affichage

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Si l'utilisateur ferme la fenêtre
                    self.stopGame()  # Arrêt de Pygame
                elif event.type == pygame.KEYDOWN:  # Si une touche est pressée
                    self.pressed[event.key] = True  # Enregistrement de la touche pressée
                    if event.key == pygame.K_ESCAPE:  # Si la touche ESCAPE est pressée
                        self.status = "menu"  # Retour au menu principal
                        is_open = False
                        modify_up_key, modify_down_key, modify_left_key, modify_right_key, modify_shoot_key = False, False, False, False, False  # Réinitialisation des variables de modification
                        
                    if modify_up_key:
                        self.controls["up_key"] = pygame.key.name(event.key)
                        modify_up_key = False
                    elif modify_down_key:
                        self.controls["down_key"] = pygame.key.name(event.key)
                        modify_down_key = False
                    elif modify_left_key:
                        self.controls["left_key"] = pygame.key.name(event.key)
                        modify_left_key = False
                    elif modify_right_key:
                        self.controls["right_key"] = pygame.key.name(event.key)
                        modify_right_key = False
                    elif modify_shoot_key:
                        self.controls["shoot_key"] = pygame.key.name(event.key)
                        modify_shoot_key = False
        
                elif event.type == pygame.KEYUP:  # Si une touche est relâchée
                    self.pressed[event.key] = False  # Enregistrement de la touche relâchée
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.width/2 - 150/2 <= event.pos[0] <= self.width/2 + 150/2 and 490 <= event.pos[1] <= 530:
                            self.is_running = True
                            is_open = False
                            self.status = "menu"
                        elif (self.width/2 - 150/2 <= event.pos[0] <= self.width/2 + 150/2 and 200 <= event.pos[1] <= 240):
                            modify_up_key = True
                            modify_down_key, modify_left_key, modify_right_key, modify_shoot_key = False, False, False, False
                        elif (self.width/2 - 150/2 <= event.pos[0] <= self.width/2 + 150/2 and 250 <= event.pos[1] <= 290):
                            modify_down_key = True
                            modify_up_key, modify_left_key, modify_right_key, modify_shoot_key = False, False, False, False
                        elif (self.width/2 - 150/2 <= event.pos[0] <= self.width/2 + 150/2 and 300 <= event.pos[1] <= 340):
                            modify_left_key = True
                            modify_up_key, modify_down_key, modify_right_key, modify_shoot_key = False, False, False, False
                        elif (self.width/2 - 150/2 <= event.pos[0] <= self.width/2 + 150/2 and 350 <= event.pos[1] <= 390):
                            modify_right_key = True
                            modify_up_key, modify_down_key, modify_left_key, modify_shoot_key = False, False, False, False
                        elif (self.width/2 - 150/2 <= event.pos[0] <= self.width/2 + 150/2 and 400 <= event.pos[1] <= 440):
                            modify_shoot_key = True
                            modify_up_key, modify_down_key, modify_left_key, modify_right_key = False, False, False, False
                        else:
                            modify_up_key, modify_down_key, modify_left_key, modify_right_key, modify_shoot_key = False, False, False, False, False

                if self.pressed.get(pygame.K_ESCAPE):
                    self.in_main_menu = True
                    is_open = False

    def playScreen(self):
        is_open = True
        write_port_mode = False  # Variable pour indiquer si le mode d'écriture est activé
        write_ip_mode = False  # Variable pour indiquer si le mode d'écriture est activé
        
        error1 = False  # Variable pour indiquer si une erreur est survenue
        error2 = False  # Variable pour indiquer si une erreur est survenue
        error3 = False  # Variable pour indiquer si une erreur est survenue
        error4 = False  # Variable pour indiquer si une erreur est survenue
        
        error1_time = None  # Initialisation du temps de l'erreur
        error2_time = None
        error3_time = None
        error4_time = None

        while is_open:

            self.screen.fill((0, 0, 0))  # Remplissage de l'écran en noir
            
            if error1 and error1_time and time.time() - error1_time < 3:  # Vérification du temps écoulé depuis l'erreur
                self.screen.blit(self.error1_surface, (self.width - self.error1_surface.get_width()-50, 35))
            
            if error2 and error2_time and time.time() - error2_time < 3:
                self.screen.blit(self.error2_surface, (self.width - self.error2_surface.get_width()-50, 35))
            
            if error3 and error3_time and time.time() - error3_time < 3:
                self.screen.blit(self.error3_surface, (self.width - self.error3_surface.get_width()-50, 35))

            if error4 and error4_time and time.time() - error4_time < 3:
                self.screen.blit(self.error4_surface, (self.width - self.error4_surface.get_width()-50, 35))

            self.screen.blit(self.main_title, (self.width/2 - self.main_title.get_width()/2, 50))  # Affichage du titre
            pygame.draw.rect(self.screen,(50,50,50),[self.width/2 - 150/2,540,150,40])
            self.screen.blit(self.main_back, (self.width/2 - self.main_back.get_width()/2, 550))  # Affichage du bouton "Retour"

            self.screen.blit(self.port_text, (self.width/2 - self.port_text.get_width()/2, 340))  # Affichage du texte port

            self.screen.blit(self.ip_text, (self.width/2 - self.ip_text.get_width()/2, 260))  # Affichage du texte ip

            pygame.draw.rect(self.screen,(50,50,50),[self.width/2 - 150/2,440,150,40])
            self.screen.blit(self.play_text, (self.width/2 - self.play_text.get_width()/2, 450))  # Affichage du texte "Rejoindre"

            pygame.draw.rect(self.screen,(50,50,50),[self.width/2 - 150/2,490,150,40])
            self.screen.blit(self.create_text, (self.width/2 - self.create_text.get_width()/2, 500))  # Affichage du texte "Créer"

            # Affichage du rectangle pour saisir l'adresse IP / port
            if write_port_mode:
                pygame.draw.rect(self.screen,(75,75,75),[self.width/2 - 300/2,370,300,40])
            else:
                pygame.draw.rect(self.screen,(50,50,50),[self.width/2 - 300/2,370,300,40])
            
            if write_ip_mode:
                pygame.draw.rect(self.screen,(75,75,75),[self.width/2 - 300/2,290,300,40])
            else:
                pygame.draw.rect(self.screen,(50,50,50),[self.width/2 - 300/2,290,300,40])

            

            port_surface = self.smallfont.render(str(self.port) , True , (255,255,255))  # Création d'une surface de texte
            self.screen.blit(port_surface, (self.width/2 - port_surface.get_width()/2, 380))  # Affichage du texte port

            ip_surface = self.smallfont.render(str(self.ip) , True , (255,255,255))  # Création d'une surface de texte
            self.screen.blit(ip_surface, (self.width/2 - ip_surface.get_width()/2, 300))  # Affichage du texte ip

            pygame.display.update()  # Mise à jour de l'affichage

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Si l'utilisateur ferme la fenêtre
                    self.stopGame()  # Arrêt de Pygame
                elif event.type == pygame.KEYDOWN:  # Si une touche est pressée
                    self.pressed[event.key] = True  # On enregistre que la touche est pressée
                    if write_port_mode:
                        if event.key == pygame.K_BACKSPACE:
                            self.port = str(self.port)[:-1]  # Suppression du dernier caractère du port
                        else:
                            self.port += event.unicode  # Ajout du caractère saisi au port
                    if write_ip_mode:
                        if event.key == pygame.K_BACKSPACE:
                            self.ip = str(self.ip)[:-1]
                        else:
                            self.ip += event.unicode
                elif event.type == pygame.KEYUP:  # Si une touche est relâchée
                    self.pressed[event.key] = False  # On enregistre que la touche n'est plus pressée
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # Vérification des clics sur les différents boutons
                        if self.width/2 - 150/2 <= event.pos[0] <= self.width/2 + 150/2 and 540 <= event.pos[1] <= 580: #clic sur le bouton retour
                            self.is_running = True
                            is_open = False
                            self.status = "menu"
                        if self.width/2 - 300/2 <= event.pos[0] <= self.width/2 - 300/2 + 300 and 370 <= event.pos[1] <= 410: #clic sur le champ port
                            write_port_mode = True  # Activation du mode d'écriture
                        else: #clic autre part
                            write_port_mode = False  # Désactivation du mode d'écriture
                        if self.width/2 - 300/2 <= event.pos[0] <= self.width/2 - 300/2 + 300 and 290 <= event.pos[1] <= 330: #clic sur le champ ip
                            write_ip_mode = True  # Activation du mode d'écriture
                        else: #clic autre part
                            write_ip_mode = False
                            
                        if self.width/2 - 150/2 <= event.pos[0] <= self.width/2 + 150/2 and 440 <= event.pos[1] <= 480: #clic sur le bouton rejoindre
                            self.port = int(self.port)
                            response = None
                            try:
                                response = requests.get(f"http://{self.ip}:5555/server/{self.port}")
                            except Exception as e:
                                error1 = True
                                error2 = False
                                error3 = False
                                error4 = False
                                error1_time = time.time()
                                error2_time = None
                                error3_time = None
                                error4_time = None
                                print("[CLIENT] Le serveur n'éxiste pas !")
                            if response != None and response.status_code == 200:
                                print("[CLIENT] Le serveur existe !")
                                connect = connect_to_server(self.port, self.ip, self.width, self.height)
                                if connect:
                                    print("[CLIENT] Connexion au serveur réussie !")
                                    self.connected = True
                                    is_open = False
                                    self.is_running = True
                                    self.status = "ingame"
                                    self.tanks = [self.createMyTank(position = (int((self.width - 265) / 2), int((self.height - 230) / 2)), direction="gauche", angle=135.), self.createEnemyTank(position=(125, 125), direction="droite", angle=0)]
                                    self.in_game = True
                                    error1 = False
                                    error2 = False
                                    error3 = False
                                    error4 = False
                                    error1_time = None
                                    error2_time = None
                                    error3_time = None
                                    error4_time = None
                                else:
                                    error1 = False
                                    error2 = True
                                    error3 = False
                                    error4 = False
                                    error1_time = None
                                    error2_time = time.time()
                                    error3_time = None
                                    error4_time = None
                                    print("[CLIENT] Serveur plein !")
                            elif response != None and response.status_code == 400:
                                error1 = False
                                error2 = False
                                error3 = True
                                error4 = False
                                error1_time = None
                                error2_time = None
                                error3_time = time.time()
                                error4_time = None
                                print("[CLIENT] Le serveur n'éxiste pas !")
                            elif response != None:
                                error1 = False
                                error2 = False
                                error3 = False
                                error4 = True
                                error1_time = None
                                error2_time = None
                                error3_time = None
                                error4_time = time.time()
                                print("[CLIENT] Une erreur est survenue !")
                                        
                        if self.width/2 - 150/2 <= event.pos[0] <= self.width/2 + 150/2 and 490 <= event.pos[1] <= 530: #clic sur le bouton créer
                            print("[CLIENT] Creating server on port " + str(self.ip) + ":" + str(self.port))
                            self.port = int(self.port)
                            response = None
                            try:
                                response = requests.post(f"http://{self.ip}:5555/server/{self.port}")
                            except Exception as e:
                                error1 = True
                                error2 = False
                                error3 = False
                                error4 = False
                                error1_time = time.time()
                                error2_time = None
                                error3_time = None
                                error4_time = None
                                print("[CLIENT] Le serveur n'éxiste pas !")
                            if response != None and response.status_code == 200:
                                print("[CLIENT] Création du serveur réussie !")
                                connect = connect_to_server(self.port, self.ip, self.width, self.height)
                                if connect:
                                    print("[CLIENT] Connexion au serveur réussie !")
                                    self.connected = True
                                    is_open = False
                                    self.is_running = True                                
                                    self.status = "ingame"
                                    self.tanks = [self.createMyTank()]
                                    self.in_game = True
                                    error1 = False
                                    error2 = False
                                    error3 = False
                                    error4 = False
                                    error1_time = None
                                    error2_time = None
                                    error3_time = None
                                    error4_time = None
                                else:
                                    error1 = False
                                    error2 = True
                                    error3 = False
                                    error4 = False
                                    error1_time = None
                                    error2_time = time.time()
                                    error3_time = None
                                    error4_time = None
                                    print("[CLIENT] Serveur plein !")
                            elif response != None and response.status_code == 400:
                                error1 = False
                                error2 = False
                                error3 = True
                                error4 = False
                                error1_time = None
                                error2_time = None
                                error3_time = time.time()
                                error4_time = None
                                print("[CLIENT] Le serveur n'éxiste pas !")
                            elif response != None:
                                error1 = False
                                error2 = False
                                error3 = False
                                error4 = True
                                error1_time = None
                                error2_time = None
                                error3_time = None
                                error4_time = time.time()
                                print("[CLIENT] Une erreur est survenue !")

                if self.pressed.get(pygame.K_ESCAPE):
                    self.in_main_menu = True
                    is_open = False
                    
    def stopGame(self):
        self.is_running = False  # Mise à jour de l'état de fonctionnement du jeu
        pygame.quit()  # Arrêt de Pygame
        if self.connected:
            close_connection(self.port, self.ip)  # Fermeture de la connexion
        print("Game stopped")  # Message d'arrêt du jeu
        sys.exit()  # Arrêt du programme
        return None
    
    def createMyTank(self, position=(125, 125), direction="droite", angle=0):
        tank = Tank(self, initial_position=position, rotation=direction)
        return (tank, TopTank(self, tank, angle=angle))
    
    def createEnemyTank(self, position=(-1, -1), direction="droite", angle=135.):
        if position == (-1, -1):
            position = (int((self.width - 265) / 2), int((self.height - 230) / 2))
        tank = Tank(self, initial_position=position, rotation=direction, image_path="assets/tank2.png")
        return (tank, TopTank(self, tank, angle=angle, image_path="assets/toptank2.png"))
    
    def pauseMenu(self):
        while self.pause:
            # Affichage du titre
            self.screen.blit(self.pause_text, (self.width/2 - self.pause_text.get_width()/2, 50))
            # Affichage du bouton "Reprendre"
            pygame.draw.rect(self.screen,(50,50,50),[self.width/2 - 150/2,290,150,40])
            self.screen.blit(self.reprendre_text, (self.width/2 - self.reprendre_text.get_width()/2, 300))
            # Affichage du bouton "Quitter"
            pygame.draw.rect(self.screen,(50,50,50),[self.width/2 - 150/2,340,150,40])
            self.screen.blit(self.quitter_text, (self.width/2 - self.quitter_text.get_width()/2, 350))
            pygame.display.update()

            data = [[self.tanks[0][0].rect.x, self.tanks[0][0].rect.y], self.tanks[0][0].rotation, self.tanks[0][1].get_angle(), [{"position": [projectile.rect.x, projectile.rect.y], "angle": projectile.angle} for projectile in self.tanks[0][0].all_projectiles], self.tanks[0][0].life, self.tanks[1][0].life, self.pause]
            if self.firstMessage:
                data = [[self.tanks[0][0].rect.x, self.tanks[0][0].rect.y], self.tanks[0][0].rotation,
                        self.tanks[0][1].get_angle(), [
                            {"position": [projectile.rect.x, projectile.rect.y], "angle": projectile.angle,
                             "id": projectile.id} for projectile in self.tanks[0][0].all_projectiles], 100, 100,
                        self.pause]
                self.firstMessage = False
            if data != None:
                send_message(data, self.port, self.ip)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stopGame()
                elif event.type == pygame.KEYDOWN:
                    self.pressed[event.key] = True
                elif event.type == pygame.KEYUP:
                    self.pressed[event.key] = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.width/2 - 150/2 <= event.pos[0] <= self.width/2 + 150/2 and 290 <= event.pos[1] <= 330:
                            self.pause = False
                        elif self.width/2 - 150/2 <= event.pos[0] <= self.width/2 + 150/2 and 340 <= event.pos[1] <= 380:
                            self.in_main_menu = True
                            self.pause = False