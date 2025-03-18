from common.ranks import ranks

# Fonction pour récupérer un rang par son nom
def get_rank(name: str) -> dict:
    res = ranks[0]
    for rank in ranks.values():
        if rank["name"] == name:
            res = rank
            break
    return res