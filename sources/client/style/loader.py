import pygame

def draw_loader(angle, surface, center, radius, color, num_circles=8):
    for i in range(num_circles):
        angle = angle + (i * 360 / num_circles)
        import math
        x = center[0] + radius * math.cos(math.radians(angle))
        y = center[1] + radius * math.sin(math.radians(angle))
        pygame.draw.circle(surface, color, (int(x), int(y)), 10)