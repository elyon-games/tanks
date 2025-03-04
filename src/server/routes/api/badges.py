from flask import jsonify, Blueprint
from server.services.database.db import badges as Badges

route_badges = Blueprint("badges", __name__)

@route_badges.route("/", methods=["GET"])
def get_badges():
    badges = Badges.get_all()
    return jsonify(badges)