from flask import jsonify, Blueprint, request
from server.services.database.db import users as User
from server.middleware.auth import login_required

route_users = Blueprint("users", __name__)

@route_users.route("/", methods=["GET"])
def get_users():
    users = User.get_all()
    users_list = []
    for user in users:
        users_list.append({
            "id": user["id"],
            "username": user["username"],
            "bio": user.get("bio", ""),
            "avatar": user.get("avatar"),
            "badges": user.get("badges", []),
        })
    return jsonify(users_list)

@route_users.route("/me", methods=["GET"])
@login_required
def get_profile():
    user = User.get_by_id(request.user_id)
    if not user:
        return jsonify({"error": "Utilisateur non trouvé"}), 404
    return jsonify({
        "id": user["id"],
        "email": user["email"],
        "username": user["username"],
        "money": user.get("money", 0.0),
        "avatar": user.get("avatar"),
        "badges": user.get("badges", []),
        "created_at": user["created_at"],
        "admin": user.get("admin", False),
        "bio": user.get("bio", ""),
    })
