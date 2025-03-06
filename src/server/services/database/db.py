from server.services.database.models import Users, Badges
from common.ranks import ranks

users = Users()
badges = Badges()

def get_user(user_id: int) -> dict:
    user = users.get(user_id)
    if not user:
        raise ValueError(f"Utilisateur avec l'id {user_id} non trouvé")
    return user

def get_user_id(username: str) -> int:
    return next((user for user in users.data if user["username"] == username), None).get("id", 0)

def get_user_badges(user_id: int) -> list:
    user = get_user(user_id)
    return [badges.get(badge_id) for badge_id in user["badges"]]

def add_user_badge(user_id: int, badge_id: str) -> None:
    user = users.get(user_id)
    badge = badges.get(badge_id)
    if not badge:
        raise ValueError(f"Badge avec l'id {badge_id} non trouvé")
    if badge_id in user["badges"]:
        raise ValueError(f"Utilisateur avec l'id {user_id} a déjà le badge avec l'id {badge_id}")
    user["badges"].append(badge_id)
    users.save()
    return user.get("badges")

def remove_user_badge(user_id: int, badge_id: str) -> None:
    user = users.get(user_id)
    badge = badges.get(badge_id)
    if not badge:
        raise ValueError(f"Badge avec l'id {badge_id} non trouvé")
    if badge_id not in user["badges"]:
        raise ValueError(f"Utilisateur avec l'id {user_id} n'a pas le badge avec l'id {badge_id}")
    user["badges"].remove(badge_id)
    users.save()
    return user.get("badges")

def get_user_stats(user_id: int) -> dict:
    user = users.get(user_id)
    kills = user.get("stats_kill", 0)
    deaths = user.get("stats_death", 0) or 1
    wins = user.get("stats_win", 0)
    loses = user.get("stats_lose", 0) or 1
    points = user.get("points", 0)

    return {
        "kills": round(kills, 1),
        "deaths": round(deaths, 1),
        "kd": round(kills / deaths, 1),
        "wins": round(wins, 1),
        "loses": round(loses, 1),
        "wl": round(wins / loses, 1),
        "points": round(points, 1)
    }

def get_user_ranks(user_id: int) -> dict:
    user = users.get(user_id)
    points = user.get("points", 0)
    return get_rank(points)

def get_rank(points: int) -> dict:
    res = ranks[0]
    for pointsMin, data in ranks.items():
        if int(pointsMin) < int(points):
            res = data
    return res["name"]

def get_classement(type: str, page: int = 1, limit: int = 10) -> list:
    valid_types = ["kills", "deaths", "kd", "wins", "loses", "wl", "points"]
    if type not in valid_types:
        raise ValueError(f"Les types valides sont: {', '.join(valid_types)}.")

    classement = []
    for user in users.data:
        user_id = user["id"]
        stats = get_user_stats(user_id)
        classement.append({
            "user_id": user_id,
            "username": user["username"],
            "value": stats[type],
            "rank": get_rank(stats["points"]),
            "points": stats["points"]
        })

    classement = sorted(classement, key=lambda x: (x["value"], x["points"]), reverse=True)
    
    start = (page - 1) * limit
    end = start + limit
    paginated_classement = classement[start:end]
    
    for i, user in enumerate(paginated_classement, start=start + 1):
        del user["points"]
        user["position"] = i
    
    return paginated_classement