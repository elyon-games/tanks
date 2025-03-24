from client.game.gameObject import GameObject  # Importe la classe GameObject du module gameObject

def getWalls(game, myMap: list, image):
    myWalls = []
    for i, lines in enumerate(myMap):
        for j, value in enumerate(lines):
            if value=="|":
                wall = GameObject(game, image_path=image, initial_position=(j*50/1080*game.height, i*50/1920*game.width), dimensions=(50/game.height, 50/game.width), custom_rotate=0, need_rotate=False)
                myWalls.append(wall)
    return myWalls