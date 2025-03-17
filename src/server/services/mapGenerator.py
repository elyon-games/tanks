import random

def generate_map(min_walls = 90, max_walls = 100) -> list:
    max_walls = random.randint(min_walls, max_walls)
    # Chargement du modèle de carte depuis le fichier mapSkeleton
    map_skeleton = [
        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', 'x', 'x', 'x', 'x', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', 'x', 'x', 'x', 'x', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', 'x', 'x', 'x', 'x', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', 'x', 'x', 'x', 'x', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'x', 'x', 'x', 'x', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'x', 'x', 'x', 'x', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'x', 'x', 'x', 'x', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'x', 'x', 'x', 'x', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-']
        ]

    # Fonction pour compter le nombre de murs adjacents à une position (i, j)
    def count_adjacent_walls(i, j):
        count = 0
        for x_offset, y_offset in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_i, new_j = i + x_offset, j + y_offset
            if 0 <= new_i < len(map_skeleton) and 0 <= new_j < len(map_skeleton[0]):
                if map_skeleton[new_i][new_j] == '|':
                    count += 1
        return count

    # Liste pour stocker les positions où des murs peuvent être ajoutés
    available_positions = []

    # Récupération des positions des cases vides pour les futurs murs
    for i in range(len(map_skeleton)):
        for j in range(len(map_skeleton[0])):
            if map_skeleton[i][j] == '-':
                available_positions.append((i, j))

    # Ajout de murs jusqu'à atteindre le nombre minimum de murs requis
    random.shuffle(available_positions)
    for _ in range(min(min_walls, len(available_positions))):
        i, j = available_positions.pop()
        map_skeleton[i][j] = '|'

    # Calcul des probabilités pour placer des murs et des espaces vides
    for i in range(len(map_skeleton)):
        for j in range(len(map_skeleton[0])):
            if map_skeleton[i][j] == '-':
                # Plus probable de placer des murs si près d'autres murs
                if random.random() < 0.6 * count_adjacent_walls(i, j) / 4:
                    map_skeleton[i][j] = '|'
                # Plus probable de placer des espaces vides sur les bords
                elif i == 0 or i == len(map_skeleton) - 1 or j == 0 or j == len(map_skeleton[0]) - 1:
                    if random.random() < 0.7:
                        map_skeleton[i][j] = '-'

    # Ajout de murs jusqu'au nombre maximum de murs autorisé
    random.shuffle(available_positions)
    for _ in range(max(0, min(max_walls - min_walls, len(available_positions)))):
        i, j = available_positions.pop()
        map_skeleton[i][j] = '|'
        
    # On compte le nombre de murs sur la carte
    wall_count = sum(line.count('|') for line in map_skeleton)
    # S'il y a trop de murs, on enlève d'abord les murs les plus isolés, puis on enlève des murs aléatoirement
    while wall_count > max_walls:
        isolated_walls = []
        for i in range(len(map_skeleton)):
            for j in range(len(map_skeleton[0])):
                if map_skeleton[i][j] == '|':
                    if count_adjacent_walls(i, j) == 0:
                        isolated_walls.append((i, j))
        if isolated_walls:
            i, j = isolated_walls.pop()
            map_skeleton[i][j] = '-'
            wall_count -= 1
        else:
            i, j = random.choice([(i, j) for i in range(len(map_skeleton)) for j in range(len(map_skeleton[0])) if map_skeleton[i][j] == '|'])
            map_skeleton[i][j] = '-'
            wall_count -= 1

    return map_skeleton
    
            
def tableauToString(map: list):
    return "\n".join("".join(line) for line in map)