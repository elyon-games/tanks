from flask import jsonify, Blueprint, request
from server.services.database.db import maps as Maps
from server.utils import formatRes

route_maps = Blueprint("api-maps", __name__)

@route_maps.route("/", methods=["GET"])
def list_maps():
    maps = [map for map in Maps.get_all()]
    return formatRes("FOUND", maps)

@route_maps.route("/<int:map_id>", methods=["GET"])
def get_map(map_id):
    map = Maps.get(map_id)
    return formatRes("FOUND", map)