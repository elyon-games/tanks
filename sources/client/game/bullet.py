import math
from client.game.movable import Movable  # Importation de la classe parente Movable

class Bullet(Movable):
    def __init__(self, game, id, velocity=20, angle=0, start=(0, 0), max_bounce=3):
        self.angle = angle
        self.max_bounce = max_bounce
        # Appel du constructeur de la classe parente (Movable)
        super().__init__(game, "bullet-lite", start, (17/1080, 17/1920), velocity, 270 - self.angle)
        
        # Angle de déplacement de la balle
        # Position de départ de la balle
        self.start = start
        self.start = (self.start[0] - 45, self.start[1] - 45)  # Ajustement de la position de départ
        # Rectangle englobant l'image de la balle
        self.rect = self.image.get_rect(center=start)
        # Vitesse de déplacement de la balle
        self.velocity = velocity
        # Référence à l'instance de la classe Game
        self.game = game

        self.rebond = 0
        
        self.id = id
        
        self.cos_angle = math.cos(math.radians(angle))
        self.sin_angle = math.sin(math.radians(angle))
        # Calcul des composantes dx et dy du déplacement de la balle
        self.dx = math.cos(math.radians(angle)) * self.velocity  # Calcul de la composante horizontale
        self.dy = math.sin(math.radians(angle)) * self.velocity  # Calcul de la composante verticale
        
        # Rotation de l'image de la balle en fonction de l'angle de déplacement
        self.spriteRotate(self.image_custom)  # Rotation de l'image de la balle
        
    def get_position_bout_bullet(self):
        # Calcule et retourne la position du bout de la balle
        center = self.rect.center
        distance = 8
        angle = math.radians(self.angle)
        return (center[0] + distance * math.cos(angle), center[1] + distance * math.sin(angle))
        

    def update(self):
        # Si le jeu n'est pas en pause
        if not self.game.freeze:
            # Déplacement de la balle
            self.move(self.dx, self.dy, self.image_custom)  # Déplacement de la balle