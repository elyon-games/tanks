from common.ranks import ranks

def get_rank(name: str) -> dict:
    res = ranks[0]
    for rank in ranks.values():
        if rank["name"] == name:
            res = rank
            break
    return res