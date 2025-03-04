from server.services.database.models import Users, Badges

users = Users()
badges = Badges()

def get_user_badges(user_id):
    user = users.get_by_id(user_id)
    if not user:
        raise ValueError(f"Utilisateur avec l'id {user_id} non trouvé")
    return [badges.get(badge_id) for badge_id in user["badges"]]

def add_user_badge(user_id, badge_id):
    user = users.get(user_id)
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
    user = users.get(user_id)
    if not user:
        raise ValueError(f"Utilisateur avec l'id {user_id} non trouvé")
    badge = badges.get(badge_id)
    if not badge:
        raise ValueError(f"Badge avec l'id {badge_id} non trouvé")
    if badge_id not in user["badges"]:
        raise ValueError(f"Utilisateur avec l'id {user_id} n'a pas le badge avec l'id {badge_id}")
    user["badges"].remove(badge_id)
    users.save()

