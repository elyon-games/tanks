from flask import jsonify, Blueprint
from server.services.database.db import users as Users
from server.services.database.db import get_classement, get_user_id, get_user_stats
from server.utils import formatRes

# print(get_user_stats(get_user_id("admin")))

route_classement = Blueprint("classement", __name__)

@route_classement.route("/<string:type>", methods=["GET"])
def get_badges(type):
    users = get_classement(type)
    return formatRes("FOUND", {
        "users": users,
        "type": type
    })