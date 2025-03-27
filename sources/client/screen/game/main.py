import pygame  # Importation de la bibliothèque Pygame pour la création de jeux
import random  # Importation de la bibliothèque random pour générer des nombres aléatoires
from client.game.tank import Tank  # Importation de la classe Tank depuis le fichier modules/tank.py
from client.game.topTank import TopTank  # Importation de la classe TopTank depuis le fichier modules/topTank.py
from client.game.bullet import Bullet  # Importation de la classe Bullet depuis le fichier modules/bullet.py
from client.game.map import getWalls
from client.style.fonts import getFontSize
from client.lib.assets import getAsset
from sources.client.lib.gateway import close_gateway, getStatus_gateway, send_message, receive_messages
# from client.lib.network import send_message, receive_messages, get_map

import pygame
from client.lib.screen.base import Screen
from client.types import WINDOW
from client.lib.parties import getPartyInfo
from client.lib.screen.controller import getArgs
from client.lib.maps import getMap
from client.lib.settings import get_controls
from client.lib.screen.controller import showScreen
from client.var import walls as wallsData 

class gameMainScreen(Screen):
    def __init__(self, window: WINDOW):
        super().__init__(window, "game-main", "Jeu")
        self.party_id = getArgs("party_id")
        self.party_info = getPartyInfo(self.party_id)
        if self.party_info is None:
            raise Exception("Party not found")
        print("[CLIENT] Party info: ", self.party_info)
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        self.map = getMap(self.party_info["map"])
        self.mapContent = self.map["content"]
        self.background = getAsset(f"map-{self.map['name']}", (self.width, self.height))
        self.time = 0  # Initialisation du temps
        self.pressed = {}  # Dictionnaire pour gérer les touches pressées
        self.freeze = False  # Mode de pause du jeu
        self.status = "wait"
        self.connected = False  # Initialisation de la variable indiquant l'état de connexion au serveur
        self.is_running = True  # Le jeu est en cours d'exécution
        self.in_game = True  # Le jeu n'est pas en cours
        self.tanks = []  # Initialisation de la liste des tanks
        self.controls = get_controls()
        self.walls = []
        self.waiting = False
        self.win = None
        self.affichFin = False
        self.firstMessage = True
        self.setFonts()
        self.tanks = [
            self.createMyTank(position = (int((self.width - 265) / 2), int((self.height - 230) / 2)), direction="gauche", angle=135.), self.createEnemyTank(position=(125, 125), direction="droite", angle=0)
        ]  # Création des tanks (joueur et ennemi)

    def setFonts(self):
        # Initialisation des polices de caractères (textes généraux)
        self.smallfont = getFontSize(35)
        self.largefont = getFontSize(75)
        self.mediumfont = getFontSize(50)
        
        # Initialisation des polices de caractères (texte d'attente)
        self.wainting_text = self.mediumfont.render("En attente d'adversaire..." , True , (255,255,255))

        # Initialisation des polices de caractères (texte de fin de partie)
        self.win_text = self.largefont.render("Victoire !" , True , (255,255,255))  # Création d'une surface de texte
        self.loose_text = self.largefont.render("Défaite !" , True , (255,255,255))  # Création d'une surface de texte
    
    def finish(self):
        if self.connected:
            close_gateway()  # Fermeture de la connexion
        for tank in self.tanks:
            tank[0].all_projectiles.empty()
            tank[1].kill()
            tank[0].kill()
        showScreen("home")

    def UpdateView(self):  # Méthode pour démarrer le jeu
        message = None  # Initialisation de la variable message (évite les erreurs de type NoneType)
        
        # Boucle principale du jeu
            
        self.surface.blit(self.background, (0,0))  # Affichage de l'image de fond

        self.connected = getStatus_gateway()  # Vérification de la connexion au serveur            

        for wall in self.walls:
            self.surface.blit(wall.image, wall.rect)
        
        if self.in_game and self.connected:
            # Envoi des données au serveur
            # Préparation des données à envoyer au serveur
            if len(self.tanks) > 1 :
                data = [[self.tanks[0][0].rect.x, self.tanks[0][0].rect.y], self.tanks[0][0].rotation, self.tanks[0][1].get_angle(), [{"position": [projectile.rect.x, projectile.rect.y], "angle": projectile.angle, "id": projectile.id} for projectile in self.tanks[0][0].all_projectiles], self.tanks[0][0].life]
            if self.firstMessage:
                data = [[self.tanks[0][0].rect.x, self.tanks[0][0].rect.y], self.tanks[0][0].rotation, self.tanks[0][1].get_angle(), [{"position": [projectile.rect.x, projectile.rect.y], "angle": projectile.angle, "id": projectile.id} for projectile in self.tanks[0][0].all_projectiles], 100, 100]
                self.firstMessage = False
            if data != None:
                send_message(data)
            message = receive_messages()
            
            # Gestion des messages reçus du serveur
            if message == "Finish":
                print("[CLIENT] Déconnexion du serveur.")
                self.finish()
        
        if self.in_game and len(self.tanks) == 1:
            
            if not self.affichFin:
                self.surface.blit(self.wainting_text, (self.width/2 - self.wainting_text.get_width()/2, 70))  # Affichage du titre
            
            self.surface.blit(self.tanks[0][0].image, self.tanks[0][0].rect)  # Affichage du Tank
            self.surface.blit(self.tanks[0][1].image, self.tanks[0][1].rect)  # Affichage du TopTank
            
            if message and type(message) != str and message[0] == "ready":
                print("[CLIENT] Un adversaire s'est connecté.")
                self.tanks.append(self.createEnemyTank())
                wallType = random.choice(wallsData)
                self.walls = getWalls(self, self.mapContent, wallType)
        
        if self.in_game and len(self.tanks) > 1:

            if self.mapContent != None:
                wallType = random.choice(wallsData)
                self.walls = getWalls(self, self.mapContent, wallType)
            
            for tank in self.tanks:
                self.surface.blit(tank[0].image, tank[0].rect)
                self.surface.blit(tank[1].image, tank[1].rect)
                tank[0].life_bar()
            
            for tank in self.tanks:
                for bullet in tank[0].all_projectiles:
                    bullet.update()
                tank[0].all_projectiles.draw(self.surface)
            
            pygame.display.update()
            
        if self.win != None:
            self.AffichageFin()

        if self.in_game and len(self.tanks) > 1:
            
            if self.tanks[0][0].life <= 0 or self.win == False:
                self.win = False
                self.surface
            
            if not self.status == "wait":
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
    
    def AffichageFin(self):
        pass

    def createMyTank(self, position=(125, 125), direction="droite", angle=0):
        tank = Tank(self, initial_position=position, rotation=direction)
        return (tank, TopTank(self, tank, angle=angle))
    
    def createEnemyTank(self, position=(-1, -1), direction="droite", angle=135.):
        if position == (-1, -1):
            position = (int((self.width - 265) / 2), int((self.height - 230) / 2))
        tank = Tank(self, initial_position=position, rotation=direction, image_path="tank-tank2")
        return (tank, TopTank(self, tank, angle=angle, image_path="tank-toptank2"))

    def HandleEvent(self, type, event):
        if type == pygame.KEYDOWN:  # Si une touche est pressée
            self.pressed[event.key] = True  # On enregistre que la touche est pressée
        elif type == pygame.KEYUP:  # Si une touche est relâchée
            self.pressed[event.key] = False  # On enregistre que la touche n'est plus pressée
        elif type == pygame.MOUSEBUTTONDOWN:
            pass
        return super().HandleEvent(type, event)