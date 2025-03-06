from flask import jsonify, Blueprint, request
from server.utils import formatRes
from server.services.database.db import users as User
from server.services.database.db import get_user_stats, get_user_id, get_rank, get_user_ranks
from server.middleware.auth import login_required

route_users = Blueprint("api-users", __name__)

def formatUserRes(user: dict) -> dict:
    user = {
        "id": user["id"],
        "email": user["email"],
        "username": user["username"],
        "money": user.get("money", 0.0),
        "badges": user.get("badges", []),
        "created_at": user["created_at"],
        "admin": user.get("admin", False),
        "stats": get_user_stats(user["id"]),
        "rank": get_rank(user.get("points", 0))
    }
    return user

@route_users.route("/", methods=["GET"])
def get_users():
    users = User.get_all()
    users_list = []
    for user in users:
        users_list.append({
            "id": user["id"],
            "username": user["username"],
            "badges": user.get("badges", []),
            "rank": get_rank(user["points"])
        })
    return formatRes("FOUND", users_list)

@route_users.route("/me", methods=["GET"])
@login_required
def get_profile_me():
    user = User.get(request.user_id)
    if not user:
        raise ValueError("NOT_FOUND")
    return formatRes("FOUND", formatUserRes(user))

@route_users.route("/<int:user_id>", methods=["GET"])
def get_profile(user_id):
    user = User.get(user_id)
    if not user:
        raise ValueError("NOT_FOUND")
    return formatRes("FOUND", formatUserRes(user))

@route_users.route("/id/<string:username>", methods=["GET"])
def get_user_by_username(username):
    user_id = get_user_id(username)
    if not user_id:
        raise ValueError("NOT_FOUND")
    return formatRes("FOUND", str(user_id))

@route_users.route("/rank/<int:user_id>", methods=["GET"])
def get_user_rank(user_id):
    return formatRes("FOUND", get_user_ranks(user_id))