import pygame  # Bibliothèque pour le développement de jeux vidéo
import math  # Fournit des fonctions mathématiques

# Classe représentant le dessus du tank
class TopTank(pygame.sprite.Sprite):
    def __init__(self, game, tank, image_path="assets/toptank.png", angle=0):
        super().__init__()  # Appel du constructeur de la classe parente (pygame.sprite.Sprite)
        self.game = game  # Référence à l'instance de la classe Game
        self.tank = tank  # Référence à l'instance de la classe Tank associée
        self.image = pygame.image.load(image_path)  # Chargement de l'image à partir du chemin spécifié
        dimensions = ((175/1080)*self.game.height, (175/1920)*self.game.width)
        self.image = pygame.transform.scale(self.image, dimensions)  # Redimensionnement de l'image aux dimensions spécifiées
        if game.debug:
            # Ajout d'une bordure rouge autour de l'image pour le mode débogage
            self.image.fill((255, 0, 0), rect=[0, 0, dimensions[0], 5])
            self.image.fill((255, 0, 0), rect=[0, 0, 5, dimensions[1]])
            self.image.fill((255, 0, 0), rect=[0, dimensions[1]-5, dimensions[0], 5])
            self.image.fill((255, 0, 0), rect=[dimensions[0]-5, 0, 5, dimensions[1]])
        self.image = pygame.transform.rotate(self.image, -90)  # Rotation initiale de l'image
        self.rect = self.image.get_rect()  # Obtention du rectangle englobant l'image (utilisé pour le positionnement et la détection des collisions)
        self.image_original = self.image  # Sauvegarde de l'image originale pour les rotations futures
        self.angle = angle  # Angle de rotation initial
        self.rotate_with_angle(angle)  # Rotation de l'image en fonction de l'angle spécifié
        self.direction = self.tank.rotation
        tank_center = (self.tank.rect.x + self.tank.rect.width / 2, self.tank.rect.y + self.tank.rect.height / 2)
        if self.direction == "haut" or self.direction == "bas":
            self.rect = self.image.get_rect(center=self.tank.rect.center)
        elif self.direction == "droite" or self.direction == "gauche":
            self.rect = self.image.get_rect(center=tank_center)
        else:
            self.rect = self.image.get_rect(center=tank_center)

    def update(self):
        self.rotate()  # Appel de la méthode pour faire tourner le tank
        self.update_position()  # Appel de la méthode pour mettre à jour la position du tank

    # Méthode pour faire tourner le dessus du tank
    def rotate(self):
        # Calcul de l'angle entre la position de la souris et la position du tank
        mouse_position = pygame.mouse.get_pos()
        player_position = self.tank.rect.center
        tank_center = (self.tank.rect.x + self.tank.rect.width / 2, self.tank.rect.y + self.tank.rect.height / 2)
        self.angle = math.atan2(mouse_position[1] - player_position[1], mouse_position[0] - player_position[0])
        self.angle = math.degrees(self.angle)
        # Rotation de l'image du tank en fonction de l'angle calculé
        self.image = pygame.transform.rotate(self.image_original, -self.angle)
        # Mise à jour du rectangle englobant pour correspondre à la nouvelle image
        self.direction = self.tank.rotation
        if self.direction == "haut" or self.direction == "bas":
            self.rect = self.image.get_rect(center=self.tank.rect.center)
        elif self.direction == "droite" or self.direction == "gauche":
            self.rect = self.image.get_rect(center=tank_center)
        else:
            self.rect = self.image.get_rect(center=tank_center)

    # Méthode pour faire tourner le dessus du tank avec un angle spécifié
    def rotate_with_angle(self, angle):
        self.direction = self.tank.rotation
        tank_center = (self.tank.rect.x + self.tank.rect.width / 2, self.tank.rect.y + self.tank.rect.height / 2)
        # Rotation de l'image du tank en fonction de l'angle spécifié
        self.image = pygame.transform.rotate(self.image_original, -angle)
        # Mise à jour du rectangle englobant pour correspondre à la nouvelle image
        if self.direction == "haut" or self.direction == "bas":
            self.rect = self.image.get_rect(center=self.tank.rect.center)
        elif self.direction == "droite" or self.direction == "gauche":
            self.rect = self.image.get_rect(center=tank_center)
        else:
            self.rect = self.image.get_rect(center=tank_center)
        self.angle = angle

    # Méthode pour mettre à jour la position du dessus du tank
    def update_position(self):
        # Mise à jour de la position du tank pour correspondre à celle du tank associé
        self.rect.center = self.tank.rect.center

    # Méthode pour obtenir l'angle actuel de rotation du dessus du tank
    def get_angle(self):
        return self.angle  # Retourne l'angle actuel de rotation du tank

    # Méthode pour obtenir la position du bout du canon du tank
    def get_position_bout_canon(self):
        # Calcule et retourne la position du bout du canon du tank
        center = self.rect.center
        distance = 75
        angle = math.radians(self.angle)
        return (center[0] + distance * math.cos(angle), center[1] + distance * math.sin(angle))