import math

# Valeur de base 
base_value = 100
# Facteur de croissance
growth_factor = 1.5

# Valeurs des rangs
rank_values = [0] + [round(base_value * math.pow(growth_factor, i), -1) for i in range(17)]

# Noms des rangs
rank_names = [
    "unranked",
    "bronze-I", "bronze-II", "bronze-III", "bronze-IV",
    "silver-I", "silver-II", "silver-III", "silver-IV",
    "gold-I", "gold-II", "gold-III", "gold-IV",
    "amethyste-I", "amethyste-II", "amethyste-III", "amethyste-IV",
    "legendary"
]

# Icônes des rangs
rank_icons = [
    "/ranks/unranked.png",
    "/ranks/bronze-1.png", "/ranks/bronze-2.png", "/ranks/bronze-3.png", "/ranks/bronze-4.png",
    "/ranks/argent-1.png", "/ranks/argent-2.png", "/ranks/argent-3.png", "/ranks/argent-4.png",
    "/ranks/gold-1.png", "/ranks/gold-2.png", "/ranks/gold-3.png", "/ranks/gold-4.png",
    "/ranks/amethyste-1.png", "/ranks/amethyste-2.png", "/ranks/amethyste-3.png", "/ranks/amethyste-4.png",
    "/ranks/legendary.png"
]

# regroupement des données
ranks = {int(rank_values[i]): {"name": rank_names[i], "icon": rank_icons[i]} for i in range(18)}