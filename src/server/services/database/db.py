from server.services.database.models import Users, Badges

users = Users()
badges = Badges()

def get_user_id(username):
    return users.get_by_username(username=username)

def get_user_badges(user_id):
    user = users.get_by_id(user_id)
    if not user:
        raise ValueError(f"Utilisateur avec l'id {user_id} non trouvé")
    return [badges.get(badge_id) for badge_id in user["badges"]]

def add_user_badge(user_id, badge_id):
    user = users.get_by_id(user_id)
    if not user:
        raise ValueError(f"Utilisateur avec l'id {user_id} non trouvé")
    badge = badges.get(badge_id)
    if not badge:
        raise ValueError(f"Badge avec l'id {badge_id} non trouvé")
    if badge_id in user["badges"]:
        raise ValueError(f"Utilisateur avec l'id {user_id} a déjà le badge avec l'id {badge_id}")
    user["badges"].append(badge_id)
    users.save()

def remove_user_badge(user_id, badge_id):
    user = users.get_by_id(user_id)
    if not user:
        raise ValueError(f"Utilisateur avec l'id {user_id} non trouvé")
    badge = badges.get(badge_id)
    if not badge:
        raise ValueError(f"Badge avec l'id {badge_id} non trouvé")
    if badge_id not in user["badges"]:
        raise ValueError(f"Utilisateur avec l'id {user_id} n'a pas le badge avec l'id {badge_id}")
    user["badges"].remove(badge_id)
    users.save()

def get_user_stats(user_id):
    user = users.get_by_id(user_id)
    if not user:
        raise ValueError(f"Utilisateur avec l'id {user_id} non trouvé")
    kills = user.get("stats_kill", 0)
    deaths = user.get("stats_death", 0) or 1
    wins = user.get("stats_win", 0)
    loses = user.get("stats_lose", 0) or 1

    return {
        "kills": kills,
        "deaths": deaths,
        "kd": kills / deaths,
        "wins": wins,
        "loses": loses,
        "wl": wins / loses
    }