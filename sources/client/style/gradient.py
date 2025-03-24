from pygame.draw import line
def draw_gradient(surface, color1, color2, width, height):
    for y in range(height):
        blend_ratio = y / height
        blended_color = (
            int(color1[0] * (1 - blend_ratio) + color2[0] * blend_ratio),
            int(color1[1] * (1 - blend_ratio) + color2[1] * blend_ratio),
            int(color1[2] * (1 - blend_ratio) + color2[2] * blend_ratio),
        )
        line(surface, blended_color, (0, y), (width, y))