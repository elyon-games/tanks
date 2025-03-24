import pygame
import math
from client.game.gameObject import GameObject  # Importe la classe GameObject du module gameObject

def Sqr(a):
    return a*a

def Distance(x1,y1,x2,y2):
    return math.sqrt(Sqr(y2-y1)+Sqr(x2-x1))

# Classe représentant un objet mobile, héritant de GameObject
class Movable(GameObject):
    # Le constructeur de la classe Movable
    def __init__(self, game, image_path, initial_position=(0, 0), dimensions=(150, 150), velocity=5, custom_rotate=0):
        # Appel du constructeur de la classe parente (GameObject)
        super().__init__(game, image_path, initial_position, dimensions, custom_rotate)
        # Initialisation de la vitesse de l'objet
        self.velocity = velocity
        # Chemin de l'image de l'objet mobile
        self.image_pathmovable = image_path


    # Méthode pour déplacer l'objet
    def move(self, dx, dy, rotate):
        if 'bullet' in self.image_pathmovable:
            # On vérifie si le futur déplacement est valide
            if not self.collisionsBullet():
                # Si on obtient False, on déplace l'objet
                self.rect.x += self.dx
                self.rect.y += self.dy
        else:
            # On vérifie si le futur déplacement est valide
            if not self.collisionsTank(dx, dy):
                # Si on obtient False, on déplace l'objet
                self.rect.x += dx
                self.rect.y += dy
                # On met à jour l'image de l'obje
                if self.get_direction(self.image) != rotate:
                    self.spriteRotate(rotate)
        
            
            
    def collisionsTank(self, dx, dy):
        # On prend la futur position du tank
        fx = self.rect.x + dx
        fy = self.rect.y + dy
        # On crée un rectangle à la position du tank
        future_rect = pygame.Rect(fx, fy, self.rect.width, self.rect.height)
        # On vérifie si le tank touche un autre tank
        for tank in self.game.tanks:
            if tank[0] != self and future_rect.colliderect(tank[0].rect):
                # On retourne True pour indiquer qu'il y a eu une collision
                return True            
        # On vérifie si le tank touche un mur
        for wall in self.game.walls:
            if future_rect.colliderect(wall.rect):
                # On cherche le côté du mur qui a été touché
                rect_center = wall.rect.center
                # On calcule la distance entre le centre du mur et le centre de chaque coté du tank
                minDist = Distance(rect_center[0], rect_center[1], self.rect.midtop[0], self.rect.midtop[1])
                side = "top"
                if Distance(rect_center[0], rect_center[1], self.rect.midleft[0], self.rect.midleft[1]) < minDist:
                    minDist = Distance(rect_center[0], rect_center[1], self.rect.midleft[0], self.rect.midleft[1])
                    side = "left"
                if Distance(rect_center[0], rect_center[1], self.rect.midright[0], self.rect.midright[1]) < minDist:
                    minDist = Distance(rect_center[0], rect_center[1], self.rect.midright[0], self.rect.midright[1])
                    side = "right"
                if Distance(rect_center[0], rect_center[1], self.rect.midbottom[0], self.rect.midbottom[1]) < minDist:
                    minDist = Distance(rect_center[0], rect_center[1], self.rect.midbottom[0], self.rect.midbottom[1])
                    side = "bottom"
                # On vérifie le déplacement du tank
                if side == "top":
                    if dy < 0:
                        return True
                if side == "bottom":
                    if dy > 0:
                        return True
                if side == "left":
                    if dx < 0:
                        return True
                if side == "right":
                    if dx > 0:
                        return True
        # On vérifie si le tank touche un bord de l'écran, de la même manière que pour les murs
        if self.rect.x + dx < 0 or self.rect.x + dx > self.game.width - self.rect.width or self.rect.y + dy < 0 or self.rect.y + dy > self.game.height - self.rect.height:
            if self.rect.x + dx < 0:
                if dx < 0:
                    return True
            if self.rect.x + dx > self.game.width - self.rect.width:
                if dx > 0:
                    return True
            if self.rect.y + dy < 0:
                if dy < 0:
                    return True
            if self.rect.y + dy > self.game.height - self.rect.height:
                if dy > 0:
                    return True
        # On retourne False pour indiquer qu'il n'y a pas eu de collision car le tank à passer tous les tests
        return False
    
    
    def collisionsBullet(self):
        # On prend la futur position de la balle
        fx = self.rect.x + self.dx
        fy = self.rect.y + self.dy
        # On crée un rectangle à la position de la balle
        future_rect = pygame.Rect(fx, fy, self.rect.width, self.rect.height)
        # On vérifie si la balle touche un tank
        for tank in self.game.tanks:
            if future_rect.colliderect(tank[0].rect):
                # On supprime la balle
                self.kill()
                # On retire des points de vie au tank
                tank[0].life -= 10
                # On retourne True pour indiquer qu'il y a eu une collision
                return True
        # On vérifie si la balle touche un bord de l'écran
        if self.rect.x < 0 or self.rect.x > self.game.width - self.rect.width or self.rect.y < 0 or self.rect.y > self.game.height - self.rect.height:
            # On regarde son compteur de rebond
            if self.rebond == self.max_bounce:
                # Si il est égal à 3, on supprime la balle
                self.kill()
            else:
                # Sinon, on l'incrémente
                self.rebond += 1
                # On regarde précisément quel bord de l'écran la balle a touché
                if self.rect.x < 0 or self.rect.x > self.game.width - self.rect.width:
                    # Si elle touche la gauche ou la droite, on inverse la composante horizontale du déplacement, on met à jour l'angle et on fait tourner l'image
                    self.dx = -self.dx
                    self.cos_angle = -self.cos_angle
                    self.angle = math.degrees(math.atan2(self.sin_angle, self.cos_angle))
                    self.newAngle(self.angle)
                    self.spriteRotate(self.angle) 
                    # On retourne False pour indiquer que le mouvement est maintenant valide
                    return False
                if self.rect.y < 0 or self.rect.y > self.game.height - self.rect.height:
                    # Si elle touche le haut ou le bas, on inverse la composante verticale du déplacement, on met à jour l'angle et on fait tourner l'image
                    self.dy = -self.dy
                    self.sin_angle = -self.sin_angle
                    self.angle = math.degrees(math.atan2(self.sin_angle, self.cos_angle))
                    self.newAngle(self.angle)
                    self.spriteRotate(self.angle)
                    # On retourne False pour indiquer que le mouvement est maintenant valide
                    return False
        # On vérifie si la balle touche un mur
        bout = self.get_position_bout_bullet()
        for wall in self.game.walls:
            if wall.rect.collidepoint(bout) or future_rect.colliderect(wall.rect):
                # On regarde son compteur de rebond
                if self.rebond == self.max_bounce:
                    # Si il est égal à 3, on supprime la balle
                    self.kill()
                else:
                    # Sinon, on l'incrémente
                    self.rebond += 1
                    # On regarde précisément quel côté du mur la balle a touché
                    rect_wall = wall.rect
                    min = 0
                    # On calcule la distance entre le bout de la balle et chaque point centré des côtés du mur
                    dist = Distance(bout[0], bout[1], rect_wall.midleft[0], rect_wall.midleft[1])
                    if dist < min or min == 0:
                        min = dist
                        side = "left"
                    dist = Distance(bout[0], bout[1], rect_wall.midright[0], rect_wall.midright[1])
                    if dist < min or min == 0:
                        min = dist
                        side = "right"
                    dist = Distance(bout[0], bout[1], rect_wall.midtop[0], rect_wall.midtop[1])
                    if dist < min or min == 0:
                        min = dist
                        side = "top"
                    dist = Distance(bout[0], bout[1], rect_wall.midbottom[0], rect_wall.midbottom[1])
                    if dist < min or min == 0:
                        min = dist
                        side = "bottom"
                    # On inverse la composante horizontale du déplacement si la balle touche le côté gauche du mur
                    if side == "left":
                        self.dx = -self.dx
                        self.cos_angle = -self.cos_angle
                        self.angle = math.degrees(math.atan2(self.sin_angle, self.cos_angle))
                        self.newAngle(self.angle)
                        self.spriteRotate(self.angle)
                    # On inverse la composante horizontale du déplacement si la balle touche le côté droit du mur
                    if side == "right":
                        self.dx = -self.dx
                        self.cos_angle = -self.cos_angle
                        self.angle = math.degrees(math.atan2(self.sin_angle, self.cos_angle))
                        self.newAngle(self.angle)
                        self.spriteRotate(self.angle)
                    # On inverse la composante verticale du déplacement si la balle touche le côté haut du mur
                    if side == "top":
                        self.dy = -self.dy
                        self.sin_angle = -self.sin_angle
                        self.angle = math.degrees(math.atan2(self.sin_angle, self.cos_angle))
                        self.newAngle(self.angle)
                        self.spriteRotate(self.angle)
                    # On inverse la composante verticale du déplacement si la balle touche le côté bas du mur
                    if side == "bottom":
                        self.dy = -self.dy
                        self.sin_angle = -self.sin_angle
                        self.angle = math.degrees(math.atan2(self.sin_angle, self.cos_angle))
                        self.newAngle(self.angle)
                        self.spriteRotate(self.angle)
                    # On retourne False pour indiquer que le mouvement est maintenant valide
                    return False
        # On retourne False pour indiquer qu'il n'y a pas eu de collision car la balle à passer tous les tests
        return False