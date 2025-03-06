from flask import jsonify, Blueprint, request
from server.services.database.db import users as Users
from server.services.database.db import get_classement
from server.utils import formatRes

route_classement = Blueprint("api-classement", __name__)
@route_classement.route("/<string:type>", methods=["GET"])
def get_badges(type):
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    return formatRes("FOUND", {
        "users": get_classement(type, page, per_page),
        "type": type,
        "page": page,
        "per_page": per_page
    })